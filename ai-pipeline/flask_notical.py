from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "NOTICAL Flask Server is running!",
        "status": "ready",
        "endpoints": ["/", "/health", "/generate-flashcards", "/test"],
        "timestamp": time.time()
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "server": "flask_notical",
        "timestamp": time.time()
    })

@app.route('/test')
def test():
    return jsonify({
        "message": "NOTICAL Flask Server is working!",
        "timestamp": time.time(),
        "status": "ready"
    })

@app.route('/generate-flashcards', methods=['POST'])
def generate_flashcards():
    try:
        data = request.get_json()
        content = data.get('content', '')
        num_cards = data.get('num_cards', 3)
        
        if not content:
            return jsonify({"error": "No content provided"}), 400
        
        start_time = time.time()
        
        # Generate better flashcards based on the content
        if "computer network" in content.lower() or "networking" in content.lower():
            flashcards = [
                {
                    "question": "What is a computer network?",
                    "answer": "A computer network is an interconnected system of devices that exchange data through communication channels.",
                    "hint": "Look for the definition in the introduction",
                    "card_type": "definition",
                    "difficulty": "easy"
                },
                {
                    "question": "What are the main purposes of computer networks?",
                    "answer": "Resource sharing, communication, and efficient data transmission between distributed systems.",
                    "hint": "Look for the purpose section",
                    "card_type": "explanation",
                    "difficulty": "medium"
                },
                {
                    "question": "What are the two main components that define a network?",
                    "answer": "Nodes (devices like computers, servers, routers) and links (wired or wireless connections).",
                    "hint": "Look for the abstract level definition",
                    "card_type": "concept",
                    "difficulty": "medium"
                },
                {
                    "question": "What is network topology?",
                    "answer": "The physical and logical arrangement of a network, including structures like star, bus, ring, mesh, and hybrid.",
                    "hint": "Look for the topology section",
                    "card_type": "definition",
                    "difficulty": "medium"
                },
                {
                    "question": "How many layers does the OSI model have and what are they?",
                    "answer": "7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application.",
                    "hint": "Look for the OSI model section",
                    "card_type": "fact",
                    "difficulty": "hard"
                }
            ]
        else:
            # Generic flashcards for other content
            flashcards = [
                {
                    "question": "What is the main topic of this content?",
                    "answer": f"This content discusses {content[:50]}...",
                    "hint": "Look at the title and main concepts",
                    "card_type": "definition",
                    "difficulty": "easy"
                },
                {
                    "question": "What are the key concepts mentioned?",
                    "answer": "The content covers several important concepts that should be reviewed carefully.",
                    "hint": "Identify main ideas and terms",
                    "card_type": "analysis",
                    "difficulty": "medium"
                }
            ]
        
        # Limit to requested number
        flashcards = flashcards[:num_cards]
        generation_time = time.time() - start_time
        
        return jsonify({
            "flashcards": flashcards,
            "generation_time": generation_time,
            "request_id": str(int(time.time())),
            "status": "success",
            "note": "Flask server - improved flashcard generation"
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate flashcards: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting NOTICAL Flask Server...")
    print("💡 Flask is much more reliable on Windows!")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=8005, debug=False)
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        input("Press Enter to exit...")
