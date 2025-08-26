#!/usr/bin/env python3
"""
NOTICAL - Enterprise-Grade AI Flashcard Learning System
Main production entry point that integrates all components
"""

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import logging
import sys
import os
from datetime import datetime
import uuid
import asyncio
from contextlib import asynccontextmanager
import json

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our enterprise-grade components
from core.config import APP_NAME, APP_VERSION, DEVICE, OFFLINE_MODE
from core.self_learning_llm import SelfLearningLLM
from training.continuous_learning import ContinuousLearningPipeline
from core.enhanced_ai_core import EnhancedNOTICALAICore

# Set up enterprise-grade logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Just console for now
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Global system components
llm: Optional[SelfLearningLLM] = None
training_pipeline: Optional[ContinuousLearningPipeline] = None
enhanced_ai: Optional[EnhancedNOTICALAICore] = None
system_ready = False

# Pydantic models for enterprise API
class FlashcardRequest(BaseModel):
    content: str = Field(..., description="Content to generate flashcards from", min_length=10)
    num_cards: int = Field(default=5, ge=1, le=20, description="Number of flashcards to generate")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    content_type: Optional[str] = Field(default="text", description="Type of content (text, pdf, audio)")
    difficulty: Optional[str] = Field(default="medium", description="Difficulty level (easy, medium, hard)")

class FlashcardResponse(BaseModel):
    flashcards: List[Dict[str, Any]]
    model_stats: Dict[str, Any]
    generation_time: float
    request_id: str
    system_status: str
    model_version: str
    content_analysis: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    flashcard_id: str = Field(..., description="ID of the flashcard")
    user_rating: int = Field(..., ge=1, le=5, description="User rating (1-5)")
    user_correction: Optional[str] = Field(None, description="User's corrected version")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    content_context: Optional[str] = Field(None, description="Original content context")
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5, description="Perceived difficulty")

class SystemStatusResponse(BaseModel):
    status: str
    components: Dict[str, str]
    model_stats: Dict[str, Any]
    training_status: Dict[str, Any]
    system_health: str
    uptime: float

class TrainingRequest(BaseModel):
    force_training: bool = Field(default=False, description="Force immediate training")
    user_id: Optional[str] = Field(None, description="User requesting training")

# Simplified startup - no async complexity
def initialize_system():
    """Initialize the system components synchronously"""
    global llm, training_pipeline, enhanced_ai, system_ready
    
    logger.info("🚀 Starting NOTICAL Enterprise System...")
    
    try:
        # Initialize core components
        logger.info("🧠 Initializing Self-Learning LLM...")
        llm = SelfLearningLLM(device=DEVICE)
        
        logger.info("🔄 Initializing Continuous Learning Pipeline...")
        training_pipeline = ContinuousLearningPipeline()
        
        logger.info("⚡ Initializing Enhanced AI Core...")
        enhanced_ai = EnhancedNOTICALAICore()
        
        system_ready = True
        logger.info("✅ NOTICAL Enterprise System initialized successfully!")
        
        # Log system stats
        stats = llm.get_model_stats()
        logger.info(f"System Stats: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ System initialization failed: {e}")
        system_ready = False
        return False

# Initialize FastAPI with enterprise features
app = FastAPI(
    title=APP_NAME,
    description="Enterprise-grade AI-powered flashcard learning system with self-learning capabilities",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Enterprise-grade middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure for production
)

# Initialize system on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the system on startup"""
    logger.info("🚀 NOTICAL Enterprise System starting up...")
    initialize_system()

# Dependency injection for system readiness
async def get_system_status():
    """Check if system is ready"""
    if not system_ready:
        raise HTTPException(
            status_code=503,
            detail="System is initializing. Please wait."
        )
    return True

# Health and status endpoints
@app.get("/", response_model=SystemStatusResponse)
async def root():
    """Root endpoint with comprehensive system status"""
    if not system_ready:
        return SystemStatusResponse(
            status="initializing",
            components={"llm": "loading", "training": "loading", "enhanced_ai": "loading"},
            model_stats={},
            training_status={},
            system_health="initializing",
            uptime=0.0
        )
    
    # Get comprehensive system status
    components = {
        "llm": "ready" if llm else "not_ready",
        "training": "ready" if training_pipeline else "not_ready",
        "enhanced_ai": "ready" if enhanced_ai else "not_ready"
    }
    
    model_stats = llm.get_model_stats() if llm else {}
    training_status = training_pipeline.get_training_status() if training_pipeline else {}
    
    return SystemStatusResponse(
        status="ready",
        components=components,
        model_stats=model_stats,
        training_status=training_status,
        system_health="healthy",
        uptime=0.0  # TODO: Implement uptime tracking
    )

@app.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/system/status")
async def system_status():
    """Detailed system status"""
    if not system_ready:
        raise HTTPException(status_code=503, detail="System initializing")
    
    return {
        "status": "ready",
        "components": {
            "llm": "ready",
            "training_pipeline": "ready",
            "enhanced_ai": "ready"
        },
        "model_info": llm.get_model_stats() if llm else {},
        "training_info": training_pipeline.get_training_status() if training_pipeline else {},
        "device": DEVICE,
        "offline_mode": OFFLINE_MODE
    }

# Core flashcard generation endpoint
@app.post("/generate-flashcards", response_model=FlashcardResponse)
async def generate_flashcards(
    request: FlashcardRequest,
    background_tasks: BackgroundTasks,
    _: bool = Depends(get_system_status)
):
    """Generate high-quality flashcards using the self-learning LLM"""
    start_time = datetime.now()
    request_id = str(uuid.uuid4())
    
    try:
        logger.info(f"🎯 Generating {request.num_cards} flashcards for user {request.user_id}")
        
        # Use enhanced AI to analyze content first
        content_analysis = None
        if enhanced_ai:
            content_analysis = enhanced_ai.analyze_content_intelligently(request.content)
            logger.info(f"📊 Content analysis: {len(content_analysis.get('key_concepts', []))} key concepts detected")
        
        # Generate flashcards using the self-learning LLM
        flashcards = llm.generate_flashcards(
            content=request.content,
            num_cards=request.num_cards
        )
        
        generation_time = (datetime.now() - start_time).total_seconds()
        
        # Get model stats
        model_stats = llm.get_model_stats() if llm else {}
        
        # Store learning example in enhanced AI core
        if enhanced_ai and content_analysis:
            enhanced_ai._store_learning_example(
                text=request.content,
                concepts=content_analysis.get('key_concepts', []),
                complexity=content_analysis.get('complexity_score', 5),
                subjects=content_analysis.get('subject_areas', [])
            )
        
        logger.info(f"✅ Generated {len(flashcards)} flashcards in {generation_time:.2f}s")
        
        return FlashcardResponse(
            flashcards=flashcards,
            model_stats=model_stats,
            generation_time=generation_time,
            request_id=request_id,
            system_status="ready",
            model_version=model_stats.get("model_name", "unknown"),
            content_analysis=content_analysis
        )
        
    except Exception as e:
        logger.error(f"❌ Flashcard generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate flashcards: {str(e)}"
        )

# Feedback collection endpoint
@app.post("/feedback")
async def collect_feedback(
    request: FeedbackRequest,
    _: bool = Depends(get_system_status)
):
    """Collect user feedback for continuous learning"""
    try:
        logger.info(f"📝 Collecting feedback for flashcard {request.flashcard_id}")
        
        # Store feedback in the training pipeline's feedback file
        if training_pipeline:
            feedback_data = {
                'flashcard_id': request.flashcard_id,
                'user_rating': request.user_rating,
                'user_correction': request.user_correction,
                'user_id': request.user_id,
                'content_context': request.content_context,
                'difficulty_rating': request.difficulty_rating,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add to feedback file
            feedback_file = "models/feedback_data.json"
            existing_feedback = []
            
            if os.path.exists(feedback_file):
                try:
                    with open(feedback_file, 'r') as f:
                        existing_feedback = json.load(f)
                except:
                    existing_feedback = []
            
            existing_feedback.append(feedback_data)
            
            with open(feedback_file, 'w') as f:
                json.dump(existing_feedback, f, indent=2)
            
            logger.info(f"✅ Feedback stored. Total feedback samples: {len(existing_feedback)}")
        
        return {"status": "feedback_collected", "message": "Feedback recorded successfully"}
        
    except Exception as e:
        logger.error(f"❌ Feedback collection failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to collect feedback: {str(e)}"
        )

# Training management endpoints
@app.post("/training/trigger")
async def trigger_training(
    request: TrainingRequest,
    _: bool = Depends(get_system_status)
):
    """Manually trigger model training"""
    try:
        logger.info(f"🔄 Manual training triggered by user {request.user_id}")
        
        if training_pipeline:
            # Check if we should train
            status = training_pipeline.get_training_status()
            if status['ready_for_training'] or request.force_training:
                # Run training cycle
                success = training_pipeline.run_continuous_learning_cycle(
                    model=llm.model,
                    tokenizer=llm.tokenizer
                )
                
                if success:
                    return {"status": "training_completed", "message": "Model training completed successfully"}
                else:
                    return {"status": "training_failed", "message": "Model training failed"}
            else:
                return {"status": "no_training_needed", "message": "Not enough feedback for training"}
        else:
            raise HTTPException(status_code=503, detail="Training pipeline not available")
            
    except Exception as e:
        logger.error(f"❌ Training trigger failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to trigger training: {str(e)}"
        )

@app.get("/training/status")
async def get_training_status():
    """Get current training status"""
    if not training_pipeline:
        raise HTTPException(status_code=503, detail="Training pipeline not available")
    
    return training_pipeline.get_training_status()

# Enhanced AI features
@app.post("/ai/analyze")
async def analyze_content(
    content: str,
    _: bool = Depends(get_system_status)
):
    """Use enhanced AI to analyze content"""
    try:
        if not enhanced_ai:
            raise HTTPException(status_code=503, detail="Enhanced AI not available")
            
        # Analyze content using enhanced AI
        analysis = enhanced_ai.analyze_content_intelligently(content)
        
        return {
            "content_analysis": analysis,
            "learning_stats": enhanced_ai.get_learning_stats()
        }
        
    except Exception as e:
        logger.error(f"❌ Content analysis failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze content: {str(e)}"
        )

@app.post("/ai/hint")
async def generate_hint(
    question: str,
    content: str,
    _: bool = Depends(get_system_status)
):
    """Generate intelligent hints for questions"""
    try:
        if not enhanced_ai:
            raise HTTPException(status_code=503, detail="Enhanced AI not available")
            
        hint = enhanced_ai.generate_intelligent_hint(question, content)
        
        return {"hint": hint}
        
    except Exception as e:
        logger.error(f"❌ Hint generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate hint: {str(e)}"
        )

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for enterprise-grade error handling"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    logger.info("🚀 Starting NOTICAL Enterprise System...")
    logger.info(f"📡 Server will be available at: http://localhost:8004")
    logger.info(f"🌐 API docs will be at: http://localhost:8004/docs")
    logger.info(f"📊 System health at: http://localhost:8004/")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=False,  # Disable reload for production
        log_level="info",
        access_log=True
    )
