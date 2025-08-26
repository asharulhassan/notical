#!/usr/bin/env python3
"""
NOTICAL Working Server - Bypasses Uvicorn Windows Issues
"""

import http.server
import socketserver
import json
import sys
import os
import time
import threading
from urllib.parse import urlparse, parse_qs
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our components
from core.self_learning_llm import SelfLearningLLM
from core.enhanced_ai_core import EnhancedNOTICALAICore

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global components
llm = None
enhanced_ai = None

class NOTICALHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP handler for NOTICAL API"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "NOTICAL AI Server is running!",
                "status": "ready",
                "endpoints": ["/", "/health", "/generate-flashcards", "/test"],
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "timestamp": time.time(),
                "llm_ready": llm is not None,
                "enhanced_ai_ready": enhanced_ai is not None
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == "/test":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "NOTICAL is working!",
                "timestamp": time.time(),
                "llm_status": "ready" if llm else "not_ready"
            }
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == "/generate-flashcards":
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "No content provided"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Read request body
            post_data = self.rfile.read(content_length)
            try:
                request_data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Invalid JSON"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # Check if LLM is ready
            if not llm:
                self.send_response(503)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "AI Model not ready"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            try:
                # Generate flashcards
                content = request_data.get('content', '')
                num_cards = request_data.get('num_cards', 5)
                
                if not content:
                    raise ValueError("No content provided")
                
                start_time = time.time()
                
                flashcards = llm.generate_flashcards(
                    content=content,
                    num_cards=num_cards
                )
                
                generation_time = time.time() - start_time
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "flashcards": flashcards,
                    "generation_time": generation_time,
                    "request_id": str(int(time.time())),
                    "status": "success"
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                logger.error(f"Flashcard generation failed: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": f"Failed to generate flashcards: {str(e)}"}
                self.wfile.write(json.dumps(response).encode())
                
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        logger.info(f"HTTP Request: {format % args}")

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

def start_server(port=8004):
    """Start the HTTP server"""
    try:
        # Initialize components first
        if not initialize_components():
            logger.error("❌ Component initialization failed!")
            return False
        
        # Create server
        with socketserver.TCPServer(("", port), NOTICALHandler) as httpd:
            logger.info(f"🚀 NOTICAL Server started successfully!")
            logger.info(f"📡 Server running at: http://localhost:{port}")
            logger.info(f"🌐 Health check: http://localhost:{port}/health")
            logger.info(f"📚 Generate flashcards: POST http://localhost:{port}/generate-flashcards")
            logger.info(f"📖 API docs: http://localhost:{port}/")
            logger.info("=" * 60)
            logger.info("🎯 Server is ready to accept requests!")
            logger.info("=" * 60)
            
            # Start server
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            logger.error(f"❌ Port {port} is already in use!")
            logger.info(f"💡 Try a different port or kill the process using port {port}")
        else:
            logger.error(f"❌ Server failed to start: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
        return True
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting NOTICAL Working Server...")
    logger.info("💡 This server bypasses Uvicorn Windows issues!")
    
    # Try to start server
    success = start_server(8004)
    
    if not success:
        logger.error("❌ Server failed to start!")
        logger.info("💡 Check the error messages above")
        sys.exit(1)
