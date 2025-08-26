# ai-pipeline/api/brand_new_api.py
"""
Brand New NOTICAL AI API - Fresh Start!
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import re

app = FastAPI(
    title="NOTICAL AI Pipeline API - BRAND NEW",
    description="Fresh AI API for intelligent flashcard generation",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlashcardRequest(BaseModel):
    content: str
    num_cards: int = 5
    generation_mode: str = "smart_understanding"

class FlashcardResponse(BaseModel):
    flashcards: List[dict]
    message: str

def generate_brand_new_flashcards(content: str, num_cards: int) -> List[dict]:
    """Generate flashcards using completely new logic"""
    
    print(f"🚀 BRAND NEW API: generate_brand_new_flashcards called!")
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    flashcards = []
    
    # Strategy 1: Find sentences that define concepts
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['is', 'are', 'means', 'refers to', 'constitutes', 'represents']):
            # Extract the subject being defined
            words = sentence.split()
            for i, word in enumerate(words):
                if (word[0].isupper() and len(word) > 2 and 
                    word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']):
                    
                    # Check if next word is a definition word
                    if i + 1 < len(words) and words[i + 1].lower() in ['is', 'are', 'means', 'refers', 'constitutes', 'represents']:
                        flashcards.append({
                            "question": f"What is {word}?",
                            "answer": sentence,
                            "type": "definition",
                            "difficulty": "medium",
                            "source": "BRAND_NEW_DEFINITION"
                        })
                        print(f"🚀 Added definition card for {word}")
                        break
    
    # Strategy 2: Find comparison sentences
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['conversely', 'however', 'while', 'whereas', 'in contrast', 'differs', 'unlike']):
            # Extract the two things being compared
            words = sentence.split()
            terms = []
            for i, word in enumerate(words):
                if (word[0].isupper() and len(word) > 2 and 
                    word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']):
                    
                    if i + 1 < len(words) and words[i + 1][0].isupper():
                        term = f"{word} {words[i + 1]}"
                        if term not in terms:
                            terms.append(term)
                    else:
                        if word not in terms:
                            terms.append(word)
            
            if len(terms) >= 2:
                flashcards.append({
                    "question": f"How do {terms[0]} and {terms[1]} differ?",
                    "answer": sentence,
                    "type": "comparison",
                    "difficulty": "hard",
                    "source": "BRAND_NEW_COMPARISON"
                })
                print(f"🚀 Added comparison card for {terms[0]} vs {terms[1]}")
    
    # Strategy 3: Find process sentences
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['relies on', 'employs', 'uses', 'implements', 'enables', 'allows', 'facilitates']):
            # Extract the main concept
            words = sentence.split()
            for i, word in enumerate(words):
                if (word[0].isupper() and len(word) > 2 and 
                    word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']):
                    
                    if i + 1 < len(words) and words[i + 1][0].isupper():
                        term = f"{word} {words[i + 1]}"
                    else:
                        term = word
                    
                    flashcards.append({
                        "question": f"How does {term} work?",
                        "answer": sentence,
                        "type": "process",
                        "difficulty": "medium",
                        "source": "BRAND_NEW_PROCESS"
                    })
                    print(f"🚀 Added process card for {term}")
                    break
    
    # Fill remaining cards with concept explanations
    remaining_cards = num_cards - len(flashcards)
    if remaining_cards > 0:
        used_sentences = set(card.get('answer', '') for card in flashcards)
        available_sentences = [s for s in sentences if s not in used_sentences and len(s) > 30]
        
        for sentence in available_sentences[:remaining_cards]:
            words = sentence.split()
            for word in words:
                if (word[0].isupper() and len(word) > 2 and 
                    word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']):
                    
                    # Check if it's part of a multi-word term
                    word_index = words.index(word)
                    if word_index + 1 < len(words) and words[word_index + 1][0].isupper():
                        term = f"{word} {words[word_index + 1]}"
                    else:
                        term = word
                    
                    flashcards.append({
                        "question": f"Explain the concept of {term} based on the context",
                        "answer": sentence,
                        "type": "concept",
                        "difficulty": "medium",
                        "source": "BRAND_NEW_CONCEPT"
                    })
                    print(f"🚀 Added concept card for {term}")
                    break
    
    print(f"🚀 BRAND NEW API: Generated {len(flashcards)} total cards")
    return flashcards[:num_cards]

@app.get("/")
async def root():
    return {"message": "BRAND NEW NOTICAL AI API is running! 🚀"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "BRAND NEW NOTICAL AI"}

@app.post("/generate", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    """Generate intelligent flashcards using brand new logic"""
    
    try:
        flashcards = generate_brand_new_flashcards(request.content, request.num_cards)
        
        return FlashcardResponse(
            flashcards=flashcards,
            message=f"Generated {len(flashcards)} intelligent flashcards using BRAND NEW logic!"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(e)}")

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "status": "success",
        "message": "BRAND NEW API is working!",
        "endpoints": ["/", "/health", "/generate", "/test"]
    }

if __name__ == "__main__":
    print("🚀 Starting BRAND NEW NOTICAL AI API on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
