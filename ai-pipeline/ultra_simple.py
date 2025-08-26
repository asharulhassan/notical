import http.server
import socketserver
import json
import time

class UltraSimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "server": "ultra_simple", "time": time.time()}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Ultra Simple Server is running!")
    
    def do_POST(self):
        if self.path == "/generate-flashcards":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    request_data = json.loads(post_data.decode('utf-8'))
                    content = request_data.get('content', '')
                    num_cards = request_data.get('num_cards', 3)
                    
                    # Generate simple flashcards
                    flashcards = [
                        {
                            "question": "What is the main topic?",
                            "answer": "Computer networks and their fundamentals",
                            "hint": "Look at the title",
                            "card_type": "definition",
                            "difficulty": "easy"
                        },
                        {
                            "question": "How many OSI layers?",
                            "answer": "7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application",
                            "hint": "Count the layers mentioned",
                            "card_type": "fact",
                            "difficulty": "medium"
                        },
                        {
                            "question": "IPv4 vs IPv6 difference?",
                            "answer": "IPv4: 32-bit (4.3 billion addresses), IPv6: 128-bit (vastly more capacity)",
                            "hint": "Look for IP addressing section",
                            "card_type": "comparison",
                            "difficulty": "medium"
                        }
                    ][:num_cards]
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    response = {
                        "flashcards": flashcards,
                        "generation_time": 0.1,
                        "status": "success",
                        "note": "Ultra simple server - no AI models"
                    }
                    self.wfile.write(json.dumps(response).encode())
                    return
                    
                except Exception as e:
                    pass
            
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Invalid request"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        print(f"Request: {format % args}")

if __name__ == "__main__":
    PORT = 8004
    print(f"🚀 Starting Ultra Simple Server on port {PORT}")
    
    try:
        with socketserver.TCPServer(("", PORT), UltraSimpleHandler) as httpd:
            print(f"✅ Server started successfully on port {PORT}")
            print(f"🌐 Health check: http://localhost:{PORT}/health")
            print(f"📚 Generate: POST http://localhost:{PORT}/generate-flashcards")
            print("=" * 50)
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        if "Address already in use" in str(e):
            print("💡 Port is already in use. Try a different port or kill the process.")
        input("Press Enter to exit...")
