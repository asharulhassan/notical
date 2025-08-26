#!/usr/bin/env python3
"""
NOTICAL Flask Server - Simple & Reliable
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import time
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our components
from core.self_learning_llm import SelfLearningLLM
from core.enhanced_ai_core import EnhancedNOTICALAICore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global components
llm = None
enhanced_ai = None

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "message": "NOTICAL AI Server is running!",
        "status": "ready",
        "endpoints": ["/", "/health", "/generate-flashcards", "/test"],
        "timestamp": time.time()
    })

@app.route('/health')
def health_check():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "llm_ready": llm is not None,
        "enhanced_ai_ready": enhanced_ai is not None
    })

@app.route('/test')
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        "message": "NOTICAL is working!",
        "timestamp": time.time(),
        "llm_status": "ready" if llm else "not_ready"
    })

@app.route('/generate-flashcards', methods=['POST'])
def generate_flashcards():
    """Generate flashcards"""
    if not llm:
        return jsonify({"error": "AI Model not ready"}), 503
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        content = data.get('content', '')
        num_cards = data.get('num_cards', 5)
        
        if not content:
            return jsonify({"error": "No content provided"}), 400
        
        logger.info(f"🎯 Generating {num_cards} flashcards...")
        
        start_time = time.time()
        
        flashcards = llm.generate_flashcards(
            content=content,
            num_cards=num_cards
        )
        
        generation_time = time.time() - start_time
        
        logger.info(f"✅ Generated {len(flashcards)} flashcards in {generation_time:.2f}s")
        
        return jsonify({
            "flashcards": flashcards,
            "generation_time": generation_time,
            "request_id": str(int(time.time())),
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}")
        return jsonify({"error": f"Failed to generate flashcards: {str(e)}"}), 500

def initialize_components():
    """Initialize AI components"""
    global llm, enhanced_ai
    
    logger.info("🧠 Loading AI Model...")
    try:
        llm = SelfLearningLLM()
        logger.info("✅ AI Model loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to load AI Model: {e}")
        return False
    
    logger.info("⚡ Loading Enhanced AI...")
    try:
        enhanced_ai = EnhancedNOTICALAICore()
        logger.info("✅ Enhanced AI loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to load Enhanced AI: {e}")
        return False
    
    return True

if __name__ == "__main__":
    logger.info("🚀 Starting NOTICAL Flask Server...")
    
    # Initialize components
    if not initialize_components():
        logger.error("❌ Component initialization failed!")
        sys.exit(1)
    
    logger.info("🚀 NOTICAL Flask Server ready!")
    logger.info(f"📡 Server will be at: http://localhost:8004")
    logger.info(f"🌐 Health check: http://localhost:8004/health")
    logger.info(f"📚 Generate flashcards: POST http://localhost:8004/generate-flashcards")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=8004, debug=False, threaded=True)
