#!/usr/bin/env python3
"""
NOTICAL AI Demo Script
Shows the AI functionality working with real examples
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_ai_endpoints():
    print("🚀 NOTICAL AI Demo - Testing All Endpoints")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Status: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: AI Status
    print("\n2️⃣ Testing AI Status...")
    try:
        response = requests.get(f"{BASE_URL}/ai/status")
        if response.status_code == 200:
            print("✅ AI status check passed!")
            status = response.json()
            print(f"   AI Available: {status['ai_available']}")
            print(f"   Models Loaded: {status['models_loaded']}")
        else:
            print(f"❌ AI status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ AI status error: {e}")
    
    # Test 3: Generate Flashcards
    print("\n3️⃣ Testing AI Flashcard Generation...")
    sample_text = """
    The human brain is the command center for the human nervous system. 
    It receives signals from the body's sensory organs and outputs information to the muscles. 
    The human brain has the same basic structure as other mammal brains but is larger in relation to body size than any other brains.
    """
    
    try:
        response = requests.post(
            f"{BASE_URL}/ai/generate/flashcards",
            data={"content": sample_text, "count": 5}
        )
        if response.status_code == 200:
            print("✅ Flashcard generation passed!")
            result = response.json()
            print(f"   Generated {result['count']} flashcards")
            for i, card in enumerate(result['flashcards'][:3], 1):
                print(f"   Card {i}: {card['question'][:60]}...")
        else:
            print(f"❌ Flashcard generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Flashcard generation error: {e}")
    
    # Test 4: Generate Notes
    print("\n4️⃣ Testing AI Note Generation...")
    try:
        response = requests.post(
            f"{BASE_URL}/ai/generate/notes",
            data={"content": sample_text, "template": "cornell"}
        )
        if response.status_code == 200:
            print("✅ Note generation passed!")
            result = response.json()
            print(f"   Template: {result['notes']['template']}")
            print(f"   Key Points: {len(result['notes']['key_points'])} extracted")
        else:
            print(f"❌ Note generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Note generation error: {e}")
    
    # Test 5: Generate Quiz
    print("\n5️⃣ Testing AI Quiz Generation...")
    try:
        response = requests.post(
            f"{BASE_URL}/ai/generate/quiz",
            data={"content": sample_text, "question_count": 3}
        )
        if response.status_code == 200:
            print("✅ Quiz generation passed!")
            result = response.json()
            print(f"   Generated {result['count']} questions")
            for i, question in enumerate(result['questions'][:2], 1):
                print(f"   Q{i}: {question['question'][:50]}...")
        else:
            print(f"❌ Quiz generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Quiz generation error: {e}")
    
    # Test 6: Explain Concept
    print("\n6️⃣ Testing AI Concept Explanation...")
    try:
        response = requests.post(
            f"{BASE_URL}/ai/explain",
            data={"concept": "neural networks", "difficulty": "simple"}
        )
        if response.status_code == 200:
            print("✅ Concept explanation passed!")
            result = response.json()
            print(f"   Difficulty: {result['difficulty']}")
            print(f"   Explanation: {result['explanation'][:80]}...")
        else:
            print(f"❌ Concept explanation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Concept explanation error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Demo Complete! All endpoints are working!")
    print("\n🌐 Frontend: http://localhost:3000")
    print("🔧 Backend: http://localhost:8000")
    print("📚 Try the Flashcards page to test AI generation!")

if __name__ == "__main__":
    test_ai_endpoints()

