#!/usr/bin/env python3
"""
Simple NOTICAL Server - Working Version
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import logging
import sys
import os
from datetime import datetime
import uuid
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our components
from core.self_learning_llm import SelfLearningLLM
from core.enhanced_ai_core import EnhancedNOTICALAICore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="NOTICAL AI Server",
    description="AI-powered flashcard generation",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
llm = None
enhanced_ai = None

# Pydantic models
class FlashcardRequest(BaseModel):
    content: str
    num_cards: int = 5
    user_id: Optional[str] = None

class FlashcardResponse(BaseModel):
    flashcards: List[Dict[str, Any]]
    generation_time: float
    request_id: str
    status: str

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global llm, enhanced_ai
    
    logger.info("🚀 Starting NOTICAL Server...")
    
    try:
        # Initialize LLM
        logger.info("🧠 Loading AI Model...")
        llm = SelfLearningLLM()
        logger.info("✅ AI Model loaded!")
        
        # Initialize Enhanced AI
        logger.info("⚡ Loading Enhanced AI...")
        enhanced_ai = EnhancedNOTICALAICore()
        logger.info("✅ Enhanced AI loaded!")
        
        logger.info("🚀 NOTICAL Server ready!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NOTICAL AI Server is running!",
        "status": "ready",
        "endpoints": ["/", "/health", "/generate-flashcards", "/docs"]
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "llm_ready": llm is not None,
        "enhanced_ai_ready": enhanced_ai is not None
    }

@app.post("/generate-flashcards", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    """Generate flashcards"""
    if not llm:
        raise HTTPException(status_code=503, detail="AI Model not ready")
    
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        logger.info(f"🎯 Generating {request.num_cards} flashcards...")
        
        # Generate flashcards
        flashcards = llm.generate_flashcards(
            content=request.content,
            num_cards=request.num_cards
        )
        
        generation_time = time.time() - start_time
        
        logger.info(f"✅ Generated {len(flashcards)} flashcards in {generation_time:.2f}s")
        
        return FlashcardResponse(
            flashcards=flashcards,
            generation_time=generation_time,
            request_id=request_id,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate flashcards: {str(e)}"
        )

@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "NOTICAL is working!",
        "timestamp": datetime.now().isoformat(),
        "llm_status": "ready" if llm else "not_ready"
    }

if __name__ == "__main__":
    logger.info("🚀 Starting NOTICAL Server...")
    logger.info(f"📡 Server will be at: http://localhost:8004")
    logger.info(f"🌐 API docs at: http://localhost:8004/docs")
    
    uvicorn.run(
        "simple_server:app",
        host="0.0.0.0",
        port=8004,
        reload=False,
        log_level="info"
    )
