import requests
import json

def test_notical_ai():
    url = "http://localhost:8004/generate-flashcards"
    
    test_content = """Computer networks are systems that connect devices to share data and resources. 
    They enable communication between computers, servers, and other devices through various protocols."""
    
    data = {
        "content": test_content,
        "num_cards": 3
    }
    
    try:
        print("🚀 Testing NOTICAL AI with content:")
        print(f"Content: {test_content[:100]}...")
        print(f"Requesting {data['num_cards']} cards...")
        
        response = requests.post(url, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! NOTICAL AI Response:")
            print(json.dumps(result, indent=2))
            
            if 'flashcards' in result:
                print(f"\n📚 Generated {len(result['flashcards'])} flashcards:")
                for i, card in enumerate(result['flashcards'], 1):
                    print(f"\nCard {i}:")
                    print(f"Q: {card.get('question', 'N/A')}")
                    print(f"A: {card.get('answer', 'N/A')}")
                    if 'hint' in card:
                        print(f"💡 Hint: {card['hint']}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_notical_ai()
