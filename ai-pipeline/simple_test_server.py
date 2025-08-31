#!/usr/bin/env python3
"""
NOTICAL Simple Test Server - No AI Models, Just Basic Functionality
"""

import http.server
import socketserver
import json
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleNOTICALHandler(http.server.BaseHTTPRequestHandler):
    """Simple HTTP handler for testing"""
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path
        
        if path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "NOTICAL Simple Test Server is running!",
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
                "server": "simple_test_server",
                "ai_models": "not_loaded_yet"
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == "/test":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "message": "NOTICAL Simple Server is working!",
                "timestamp": time.time(),
                "status": "ready"
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
        path = self.path
        
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
            
            try:
                # Generate simple test flashcards
                content = request_data.get('content', '')
                num_cards = request_data.get('num_cards', 5)
                
                if not content:
                    raise ValueError("No content provided")
                
                start_time = time.time()
                
                # Simple test flashcards (not AI-generated yet)
                test_flashcards = [
                    {
                        "question": "What is the main topic of this content?",
                        "answer": "This content discusses computer networks and their fundamentals.",
                        "hint": "Look at the title and main concepts mentioned",
                        "card_type": "definition",
                        "difficulty": "easy"
                    },
                    {
                        "question": "How many layers does the OSI model have?",
                        "answer": "The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application.",
                        "hint": "Count the layers mentioned in the content",
                        "card_type": "fact",
                        "difficulty": "medium"
                    },
                    {
                        "question": "What is the difference between IPv4 and IPv6?",
                        "answer": "IPv4 uses 32-bit addresses (about 4.3 billion unique addresses), while IPv6 uses 128-bit addresses for vastly more capacity.",
                        "hint": "Look for the IP addressing section",
                        "card_type": "comparison",
                        "difficulty": "medium"
                    }
                ]
                
                # Limit to requested number
                flashcards = test_flashcards[:num_cards]
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
                    "status": "success",
                    "note": "These are test flashcards. AI model not loaded yet."
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

def start_simple_server(port=8004):
    """Start the simple test server"""
    try:
        # Create server
        with socketserver.TCPServer(("", port), SimpleNOTICALHandler) as httpd:
            logger.info(f"🚀 NOTICAL Simple Test Server started successfully!")
            logger.info(f"📡 Server running at: http://localhost:{port}")
            logger.info(f"🌐 Health check: http://localhost:{port}/health")
            logger.info(f"📚 Generate flashcards: POST http://localhost:{port}/generate-flashcards")
            logger.info("=" * 60)
            logger.info("🎯 Simple server is ready for testing!")
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
    logger.info("🚀 Starting NOTICAL Simple Test Server...")
    logger.info("💡 This server has NO AI models - just basic functionality!")
    
    # Try to start server
    success = start_simple_server(8004)
    
    if not success:
        logger.error("❌ Server failed to start!")
        sys.exit(1)
