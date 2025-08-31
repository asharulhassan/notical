# ai-pipeline/api/main.py
"""
NOTICAL AI Pipeline API
=======================
Clean, focused API for AI operations only.
Separated from website for modular development.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uvicorn
from pydantic import BaseModel
import asyncio
import logging
import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Fix import paths - we're in api/ directory, need to go up to ai-pipeline root
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_pipeline_root = os.path.dirname(current_dir)
core_path = os.path.join(ai_pipeline_root, 'core')
sys.path.insert(0, ai_pipeline_root)
sys.path.insert(0, current_dir)  # Add current directory for local imports

try:
    from core.generator import SmartFlashcardGenerator
    from core.enhanced_ai_core import enhanced_ai_core
    import training_api
    training_router = training_api.router
    logger = logging.getLogger(__name__)
    logger.info("✅ All imports successful")
    logger.info(f"📁 AI Pipeline root: {ai_pipeline_root}")
    logger.info(f"📁 Core path: {core_path}")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Import error: {e}")
    logger.info("Current working directory: %s", os.getcwd())
    logger.info("AI Pipeline root: %s", ai_pipeline_root)
    logger.info("Python path: %s", core_path)
    logger.info("Python path: %s", sys.path)
    raise

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NOTICAL AI Pipeline API",
    description="Dedicated AI pipeline for flashcard generation and content analysis",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include training router
app.include_router(training_router)

class FlashcardRequest(BaseModel):
    content: str
    subject: Optional[str] = None
    card_types: List[str] = ["definition", "explanation", "cloze", "comparison", "analysis"]
    num_cards: int = 5
    difficulty_balance: str = "balanced"
    
    # Enhanced AI generation options
    generation_mode: str = "text_understanding"  # text_understanding, strict_text, online_research
    style: str = "professional"  # professional, simple, exam_focused
    include_online: bool = False
    exam_board: Optional[str] = None
    learning_level: str = "university"

class FlashcardResponse(BaseModel):
    flashcards: List[dict]
    subject: str
    total_generated: int
    processing_time: float
    ai_analysis: dict

class ContentAnalysisRequest(BaseModel):
    content: str
    analysis_type: str = "full"  # full, concepts, complexity, subject

class ContentAnalysisResponse(BaseModel):
    analysis: dict
    processing_time: float

# NEW: Training and Rating Models
class FlashcardRating(BaseModel):
    flashcard_id: str
    question: str
    answer: str
    user_rating: int  # 1-5 scale
    user_feedback: Optional[str] = None
    difficulty_rating: Optional[int] = None  # 1-5 scale
    clarity_rating: Optional[int] = None  # 1-5 scale
    relevance_rating: Optional[int] = None  # 1-5 scale
    content_source: str  # The original text used to generate this card

class TrainingDataRequest(BaseModel):
    content: str
    good_cards: List[dict]  # Cards that worked well
    bad_cards: List[dict]   # Cards that didn't work well
    subject: Optional[str] = None
    difficulty_level: Optional[str] = None

class TrainingResponse(BaseModel):
    success: bool
    message: str
    training_stats: dict
    model_improvement: bool

@app.get("/")
async def root():
    return {
        "message": "NOTICAL AI Pipeline API",
        "version": "2.0.0",
        "status": "active"
    }

@app.post("/generate", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    """Generate intelligent flashcards using Enhanced AI Core"""
    try:
        start_time = asyncio.get_event_loop().time()
        
        # Use Enhanced AI Core for intelligent content analysis
        content_analysis = enhanced_ai_core.analyze_content_intelligently(request.content)
        
        # Generate flashcards using the enhanced generator
        generator = SmartFlashcardGenerator()
        flashcards = generator.generate_flashcards(
            chunk={"text": request.content, "analysis": content_analysis},
            mode=request.generation_mode,
            style=request.style,
            include_online=request.include_online,
            exam_board=request.exam_board,
            level=request.learning_level,
            target_count=request.num_cards
        )
        
        # Add unique IDs for rating system
        for i, card in enumerate(flashcards):
            card['id'] = f"card_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"
            card['content_source'] = request.content[:100] + "..." if len(request.content) > 100 else request.content
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return FlashcardResponse(
            flashcards=flashcards,
            subject=request.subject or "general",
            total_generated=len(flashcards),
            processing_time=processing_time,
            ai_analysis=content_analysis
        )
        
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate flashcards: {str(e)}")

@app.post("/analyze", response_model=ContentAnalysisResponse)
async def analyze_content(request: ContentAnalysisRequest):
    """Analyze content using Enhanced AI Core"""
    try:
        start_time = asyncio.get_event_loop().time()
        
        # Use Enhanced AI Core for analysis
        analysis = enhanced_ai_core.analyze_content_intelligently(request.content)
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return ContentAnalysisResponse(
            analysis=analysis,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error analyzing content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze content: {str(e)}")

# NEW: Rating and Feedback Endpoints
@app.post("/rate")
async def rate_flashcard(rating: FlashcardRating):
    """Rate a flashcard to help the AI learn"""
    try:
        # Load existing training data
        from training_api import TRAINING_DATA_FILE
        with open(TRAINING_DATA_FILE, 'r') as f:
            training_data = json.load(f)
        
        # Add the rating
        rating_data = rating.dict()
        rating_data['timestamp'] = datetime.now().isoformat()
        training_data['user_feedback'].append(rating_data)
        
        # Update statistics
        training_data['statistics']['total_cards_rated'] += 1
        if rating.user_rating >= 4:
            training_data['statistics']['positive_ratings'] += 1
        else:
            training_data['statistics']['negative_ratings'] += 1
        
        # Save updated data
        with open(TRAINING_DATA_FILE, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        # Check if we should trigger model improvement (every 10 negative ratings)
        if training_data['statistics']['negative_ratings'] % 10 == 0:
            await trigger_model_improvement(training_data)
            training_data['statistics']['improvement_cycles'] += 1
        
        return {
            "success": True,
            "message": "Rating saved successfully",
            "total_rated": training_data['statistics']['total_cards_rated'],
            "improvement_triggered": training_data['statistics']['negative_ratings'] % 10 == 0
        }
        
    except Exception as e:
        logger.error(f"Error saving rating: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save rating: {str(e)}")

@app.post("/add_training_data", response_model=TrainingResponse)
async def add_training_data(request: TrainingDataRequest):
    """Add training data to improve the AI model"""
    try:
        # Load existing training data
        from training_api import TRAINING_DATA_FILE
        with open(TRAINING_DATA_FILE, 'r') as f:
            training_data = json.load(f)
        
        # Add training session
        training_session = {
            "timestamp": datetime.now().isoformat(),
            "content": request.content[:500] + "..." if len(request.content) > 500 else request.content,
            "subject": request.subject,
            "difficulty_level": request.difficulty_level,
            "good_cards_count": len(request.good_cards),
            "bad_cards_count": len(request.bad_cards),
            "good_cards": request.good_cards,
            "bad_cards": request.bad_cards
        }
        
        training_data['training_sessions'].append(training_session)
        
        # Save updated data
        with open(TRAINING_DATA_FILE, 'w') as f:
            json.dump(training_data, f, indent=2)
        
        # Trigger immediate model improvement
        improvement_made = await trigger_model_improvement(training_data)
        
        return TrainingResponse(
            success=True,
            message="Training data added successfully",
            training_stats={
                "total_sessions": len(training_data['training_sessions']),
                "total_feedback": training_data['statistics']['total_cards_rated'],
                "improvement_cycles": training_data['statistics']['improvement_cycles']
            },
            model_improvement=improvement_made
        )
        
    except Exception as e:
        logger.error(f"Error adding training data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add training data: {str(e)}")

@app.get("/training/stats")
async def get_training_stats():
    """Get training statistics and progress"""
    try:
        from training_api import TRAINING_DATA_FILE
        with open(TRAINING_DATA_FILE, 'r') as f:
            training_data = json.load(f)
        
        return {
            "statistics": training_data['statistics'],
            "recent_feedback": training_data['user_feedback'][-10:] if training_data['user_feedback'] else [],
            "recent_sessions": training_data['training_sessions'][-5:] if training_data['training_sessions'] else [],
            "total_training_data": len(training_data['training_sessions']),
            "model_ready_for_improvement": training_data['statistics']['negative_ratings'] >= 10
        }
        
    except Exception as e:
        logger.error(f"Error getting training stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get training stats: {str(e)}")

async def trigger_model_improvement(training_data: dict) -> bool:
    """Trigger model improvement based on user feedback"""
    try:
        logger.info("🚀 Triggering model improvement...")
        
        # Analyze recent negative feedback
        recent_negative = [f for f in training_data['user_feedback'][-20:] if f.get('user_rating', 5) < 4]
        
        if len(recent_negative) >= 5:
            # Identify common issues
            common_issues = analyze_common_issues(recent_negative)
            
            # Apply improvements to the AI core
            enhanced_ai_core.apply_improvements(common_issues)
            
            # Record the improvement
            improvement_record = {
                "timestamp": datetime.now().isoformat(),
                "trigger": "negative_feedback_threshold",
                "issues_addressed": common_issues,
                "feedback_count": len(recent_negative)
            }
            
            training_data['model_improvements'].append(improvement_record)
            
            # Save updated data
            from training_api import TRAINING_DATA_FILE
            with open(TRAINING_DATA_FILE, 'w') as f:
                json.dump(training_data, f, indent=2)
            
            logger.info(f"✅ Model improvement applied: {len(common_issues)} issues addressed")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error in model improvement: {e}")
        return False

def analyze_common_issues(negative_feedback: List[dict]) -> List[str]:
    """Analyze common issues from negative feedback"""
    issues = []
    
    # Analyze ratings
    low_clarity = [f for f in negative_feedback if f.get('clarity_rating', 5) < 3]
    low_relevance = [f for f in negative_feedback if f.get('relevance_rating', 5) < 3]
    low_difficulty = [f for f in negative_feedback if f.get('difficulty_rating', 5) < 3]
    
    if len(low_clarity) > len(negative_feedback) * 0.3:
        issues.append("improve_question_clarity")
    
    if len(low_relevance) > len(negative_feedback) * 0.3:
        issues.append("improve_content_relevance")
    
    if len(low_difficulty) > len(negative_feedback) * 0.3:
        issues.append("adjust_difficulty_assessment")
    
    return issues

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "NOTICAL AI Pipeline API",
        "version": "2.0.0"
    }

@app.get("/ai/status")
async def get_ai_status():
    """Get AI pipeline status and capabilities"""
    try:
        # Import training stats
        from training_api import TRAINING_DATA_FILE
        
        # Load training data for stats
        if TRAINING_DATA_FILE.exists():
            with open(TRAINING_DATA_FILE, 'r') as f:
                training_data = json.load(f)
        else:
            training_data = {"statistics": {"total_cards_rated": 0, "positive_ratings": 0, "negative_ratings": 0, "improvement_cycles": 0}}
        
        return {
            "ai_available": True,
            "pipeline": "NOTICAL AI Pipeline v2.0",
            "components": {
                "ai_core": "✅ Enhanced AI Core",
                "generator": "✅ SmartFlashcardGenerator",
                "training": "✅ Training Pipeline Active",
                "rating_system": "✅ User Feedback Collection"
            },
            "capabilities": [
                "Intelligent Content Analysis",
                "Context-Aware Flashcard Generation",
                "Multiple Generation Modes",
                "Difficulty Assessment",
                "Subject Detection",
                "Process & Comparison Extraction",
                "User Feedback Learning",
                "Automatic Model Improvement"
            ],
            "training_ready": True,
            "model_status": "Learning from user feedback",
            "learning_stats": {
                "total_cards_rated": training_data['statistics']['total_cards_rated'],
                "positive_ratings": training_data['statistics']['positive_ratings'],
                "negative_ratings": training_data['statistics']['negative_ratings'],
                "improvement_cycles": training_data['statistics']['improvement_cycles']
            }
        }
    except Exception as e:
        logger.error(f"Error getting AI status: {e}")
        return {
            "ai_available": False,
            "error": str(e)
        }

@app.get("/models/status")
async def get_models_status():
    """Get status of AI models"""
    try:
        from training_api import TRAINING_DATA_FILE
        
        if TRAINING_DATA_FILE.exists():
            with open(TRAINING_DATA_FILE, 'r') as f:
                training_data = json.load(f)
        else:
            training_data = {"statistics": {"total_cards_rated": 0, "positive_ratings": 0, "negative_ratings": 0, "improvement_cycles": 0}}
        
        return {
            "models": {
                "flashcard_generator": {
                    "status": "active",
                    "version": "2.0.0",
                    "training_ready": True,
                    "learning_progress": training_data['statistics']['improvement_cycles']
                },
                "content_analyzer": {
                    "status": "active",
                    "version": "2.0.0",
                    "training_ready": True,
                    "learning_progress": training_data['statistics']['improvement_cycles']
                }
            },
            "training_pipeline": "active",
            "model_storage": "local",
            "user_feedback": {
                "total_rated": training_data['statistics']['total_cards_rated'],
                "success_rate": f"{(training_data['statistics']['positive_ratings'] / max(training_data['statistics']['total_cards_rated'], 1)) * 100:.1f}%"
            }
        }
    except Exception as e:
        logger.error(f"Error getting models status: {e}")
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
