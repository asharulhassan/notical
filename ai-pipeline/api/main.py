# ai-pipeline/api/main.py
"""
NOTICAL AI Pipeline API
=======================
Clean, focused API for AI operations only.
Separated from website for modular development.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
from pydantic import BaseModel
import asyncio
import logging
import sys
import os

# Fix import paths - we're in api/ directory, need to go up to ai-pipeline root
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_pipeline_root = os.path.dirname(current_dir)
core_path = os.path.join(ai_pipeline_root, 'core')
sys.path.insert(0, ai_pipeline_root)

try:
    from core.generator import SmartFlashcardGenerator
    from core.enhanced_ai_core import enhanced_ai_core
    logger = logging.getLogger(__name__)
    logger.info("✅ All imports successful")
    logger.info(f"📁 AI Pipeline root: {ai_pipeline_root}")
    logger.info(f"📁 Core path: {core_path}")
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Import error: {e}")
    logger.info("Current working directory: %s", os.getcwd())
    logger.info("AI Pipeline root: %s", ai_pipeline_root)
    logger.info("Core path: %s", core_path)
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

# Note: Training routes will be added later once basic API is working

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

@app.get("/")
async def root():
    return {
        "message": "NOTICAL AI Pipeline API",
        "version": "2.0.0",
        "status": "active"
    }

@app.post("/generate", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    """Generate high-quality flashcards using enhanced AI"""
    try:
        start_time = asyncio.get_event_loop().time()
        
        # Use Enhanced AI Core for content analysis
        content_analysis = enhanced_ai_core.analyze_content_intelligently(request.content)
        
        # Generate flashcards using enhanced generator
        chunk = {
            "id": "generated_chunk",
            "text": request.content.strip(),
            "type": "text"
        }
        
        target_count = request.num_cards if request.num_cards > 0 else 50
        
        generator = SmartFlashcardGenerator()
        raw_cards = generator.generate_flashcards(
            chunk=chunk,
            mode=request.generation_mode,
            style=request.style,
            include_online=request.include_online,
            exam_board=request.exam_board,
            level=request.learning_level,
            target_count=target_count
        )
        
        # Convert to expected format
        flashcards = []
        for card in raw_cards[:request.num_cards]:
            difficulty_num = card.get("difficulty", 3)
            difficulty_str = "easy" if difficulty_num <= 2 else "medium" if difficulty_num <= 3 else "hard"
            
            # Generate intelligent hint based on actual content
            intelligent_hint = enhanced_ai_core.generate_intelligent_hint(card["front"], request.content)
            
            flashcards.append({
                "question": card["front"],
                "answer": card["back"],
                "type": card["type"],
                "difficulty": difficulty_str,
                "hint": intelligent_hint,
                "confidence_score": 0.9,
                "style": card.get("style", "professional"),
                "exam_board": card.get("exam_board"),
                "learning_level": card.get("level", "university"),
                "concept": card.get("concept"),
                "ai_enhanced": card.get("ai_enhanced", False)
            })
        
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
        learning_stats = enhanced_ai_core.get_learning_stats()
        return {
            "ai_available": True,
            "pipeline": "NOTICAL AI Pipeline v2.0",
            "components": {
                "ai_core": "✅ Enhanced AI Core",
                "generator": "✅ SmartFlashcardGenerator",
                "models": "🔄 Training Ready",
                "training": "🔄 Training Pipeline Ready"
            },
            "capabilities": [
                "Intelligent Content Analysis",
                "Context-Aware Flashcard Generation",
                "Multiple Generation Modes",
                "Difficulty Assessment",
                "Subject Detection",
                "Process & Comparison Extraction"
            ],
            "training_ready": True,
            "model_status": "Ready for training",
            "learning_stats": learning_stats
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
    return {
        "models": {
            "flashcard_generator": {
                "status": "active",
                "version": "2.0.0",
                "training_ready": True
            },
            "content_analyzer": {
                "status": "active",
                "version": "2.0.0",
                "training_ready": True
            }
        },
        "training_pipeline": "ready",
        "model_storage": "local"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
