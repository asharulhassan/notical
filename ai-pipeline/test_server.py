#!/usr/bin/env python3
"""
Test NOTICAL Server - Start and Test Immediately
"""

import requests
import time
import threading
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_server():
    """Start the working server in a thread"""
    os.system("python working_server.py")

def test_server():
    """Test the server"""
    print("🧪 Testing NOTICAL Server...")
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        print("🔍 Testing health endpoint...")
        response = requests.get("http://localhost:8004/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working!")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
        # Test root endpoint
        print("🔍 Testing root endpoint...")
        response = requests.get("http://localhost:8004/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
            
        # Test flashcard generation
        print("🔍 Testing flashcard generation...")
        test_data = {
            "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data.",
            "num_cards": 3
        }
        
        response = requests.post(
            "http://localhost:8004/generate-flashcards",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Flashcard generation working!")
            result = response.json()
            print(f"📊 Generated {len(result['flashcards'])} flashcards in {result['generation_time']:.2f}s")
            
            for i, card in enumerate(result['flashcards'], 1):
                print(f"📝 Card {i}: Q: {card.get('question', 'N/A')}")
                print(f"        A: {card.get('answer', 'N/A')}")
        else:
            print(f"❌ Flashcard generation failed: {response.status_code}")
            print(f"📊 Error: {response.text}")
            return False
            
        print("\n🎉" + "="*60)
        print("🎉                    SERVER TEST PASSED!                    🎉")
        print("🎉" + "="*60)
        print("✅ Your NOTICAL server is working perfectly!")
        print("🚀 You can now integrate this with your website!")
        print(f"📡 Server URL: http://localhost:8004")
        print(f"📚 API Endpoint: POST http://localhost:8004/generate-flashcards")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 NOTICAL Server Test - Start and Test Immediately")
    print("=" * 60)
    
    # Start server in background
    print("🔄 Starting server in background...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test the server
    if test_server():
        print("\n🎯 Server is ready for your website!")
        print("💡 Keep this terminal open to keep the server running")
        print("🛑 Press Ctrl+C to stop the server")
        
        try:
            # Keep server running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
    else:
        print("\n❌ Server test failed!")
        sys.exit(1)
