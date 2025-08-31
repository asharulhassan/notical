#!/usr/bin/env python3
"""
Test NOTICAL API Endpoints
"""

import requests
import json

def test_api():
    """Test all API endpoints"""
    base_url = "http://localhost:8004"
    
    print("🧪 Testing NOTICAL API Endpoints")
    print("=" * 50)
    
    # Test 1: Health Check
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
        return False
    
    # Test 2: Root Endpoint
    print("\n🔍 Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root Endpoint: PASSED")
            print(f"📊 Response: {response.json()}")
        else:
            print(f"❌ Root Endpoint: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Root Endpoint: ERROR - {e}")
        return False
    
    # Test 3: Flashcard Generation
    print("\n🔍 Testing Flashcard Generation...")
    test_data = {
        "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. It enables computers to improve their performance on a specific task without being explicitly programmed for that task.",
        "num_cards": 3
    }
    
    try:
        response = requests.post(
            f"{base_url}/generate-flashcards",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Flashcard Generation: PASSED")
            result = response.json()
            print(f"📊 Generated {len(result['flashcards'])} flashcards in {result['generation_time']:.2f}s")
            
            print("\n📚 Generated Flashcards:")
            for i, card in enumerate(result['flashcards'], 1):
                print(f"📝 Card {i}:")
                print(f"   Q: {card.get('question', 'N/A')}")
                print(f"   A: {card.get('answer', 'N/A')}")
                print()
        else:
            print(f"❌ Flashcard Generation: FAILED ({response.status_code})")
            print(f"📊 Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Flashcard Generation: ERROR - {e}")
        return False
    
    print("\n🎉" + "="*50)
    print("🎉              ALL TESTS PASSED!              🎉")
    print("🎉" + "="*50)
    print("✅ Your NOTICAL server is working perfectly!")
    print("🚀 You can now integrate this with your website!")
    print(f"📡 Server URL: {base_url}")
    print(f"📚 API Endpoint: POST {base_url}/generate-flashcards")
    
    return True

if __name__ == "__main__":
    if test_api():
        print("\n🎯 Server is ready for your website!")
    else:
        print("\n❌ Some tests failed!")
        exit(1)
