# ai-pipeline/api/simple_api.py
"""
Simple NOTICAL AI API - Now with actual content analysis!
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import re
import random

app = FastAPI(
    title="NOTICAL AI Pipeline API",
    description="AI API for intelligent flashcard generation",
    version="1.0.0"
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

def analyze_content_intelligently(text: str) -> dict:
    """Actually analyze the content to extract meaningful information"""
    
    # Extract key concepts and terms
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    # Find technical terms (words that start with capital letters or are in quotes)
    technical_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    technical_terms = list(set(technical_terms))[:15]  # Limit to 15 unique terms
    
    # Find definitions (sentences with "is", "are", "refers to", "means", etc.)
    definition_patterns = [
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are|refers\s+to|means?|constitutes|represents)\s+([^.!?]+)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:]\s*([^.!?]+)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[-]\s*([^.!?]+)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,?\s+(?:which|that)\s+([^.!?]+)'
    ]
    
    definitions = []
    for pattern in definition_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for term, definition in matches:
            # Only keep definitions that are complete and meaningful
            if len(definition.strip()) > 15 and not definition.strip().startswith(','):
                definitions.append((term, definition))
    
    # Find comparisons and contrasts
    comparison_patterns = [
        r'([^.!?]*(?:conversely|in contrast|however|while|whereas|on the other hand)[^.!?]*)',
        r'([^.!?]*(?:differs? from|unlike|compared to|versus)[^.!?]*)',
        r'([^.!?]*(?:both|similarly|likewise|also)[^.!?]*)'
    ]
    
    comparisons = []
    for pattern in comparison_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        comparisons.extend([m.strip() for m in matches if len(m.strip()) > 20])
    
    # Find processes and mechanisms
    process_patterns = [
        r'([^.!?]*(?:relies on|employs|uses|implements|employs|utilizes)[^.!?]*)',
        r'([^.!?]*(?:process|mechanism|method|technique|approach)[^.!?]*)',
        r'([^.!?]*(?:enables|allows|facilitates|provides)[^.!?]*)'
    ]
    
    processes = []
    for pattern in process_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        processes.extend([m.strip() for m in matches if len(m.strip()) > 20])
    
    return {
        'sentences': sentences,
        'technical_terms': technical_terms,
        'definitions': definitions,
        'comparisons': comparisons,
        'processes': processes,
        'word_count': len(text.split()),
        'complexity': 'high' if len(text.split()) > 200 else 'medium' if len(text.split()) > 100 else 'easy'
    }

def generate_intelligent_flashcards_v2(content: str, num_cards: int) -> List[dict]:
    """Generate flashcards based on intelligent sentence analysis - V2"""
    
    print(f"🔍 DEBUG: generate_intelligent_flashcards_v2 called with {len(content)} chars, {num_cards} cards")
    
    # Split into sentences and clean them
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    print(f"🔍 DEBUG: Found {len(sentences)} sentences")
    
    flashcards = []
    
    # Strategy 1: Find sentences that define concepts
    definition_sentences = []
    for sentence in sentences:
        # Look for sentences that define something
        if any(word in sentence.lower() for word in ['is', 'are', 'means', 'refers to', 'constitutes', 'represents']):
            # Extract the subject being defined
            words = sentence.split()
            for i, word in enumerate(words):
                if word[0].isupper() and len(word) > 2 and word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']:
                    # Check if next word is a definition word
                    if i + 1 < len(words) and words[i + 1].lower() in ['is', 'are', 'means', 'refers', 'constitutes', 'represents']:
                        definition_sentences.append((word, sentence))
                        print(f"🔍 DEBUG: Found definition: {word}")
                        break
    
    print(f"🔍 DEBUG: Found {len(definition_sentences)} definition sentences")
    
    # Strategy 2: Find comparison sentences
    comparison_sentences = []
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['conversely', 'however', 'while', 'whereas', 'in contrast', 'differs', 'unlike']):
            comparison_sentences.append(sentence)
            print(f"🔍 DEBUG: Found comparison: {sentence[:50]}...")
    
    print(f"🔍 DEBUG: Found {len(comparison_sentences)} comparison sentences")
    
    # Strategy 3: Find process/mechanism sentences
    process_sentences = []
    for sentence in sentences:
        if any(word in sentence.lower() for word in ['relies on', 'employs', 'uses', 'implements', 'enables', 'allows', 'facilitates']):
            process_sentences.append(sentence)
            print(f"🔍 DEBUG: Found process: {sentence[:50]}...")
    
    print(f"🔍 DEBUG: Found {len(process_sentences)} process sentences")
    
    # Generate cards from definition sentences
    for term, sentence in definition_sentences[:num_cards//3]:
        if term and len(term) > 2:
            flashcards.append({
                "question": f"What is {term}?",
                "answer": sentence,
                "type": "definition",
                "difficulty": "medium",
                "source": "definition_analysis"
            })
            print(f"🔍 DEBUG: Added definition card for {term}")
    
    # Generate cards from comparison sentences
    for sentence in comparison_sentences[:num_cards//4]:
        # Extract the two things being compared
        words = sentence.split()
        terms = []
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2 and word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']:
                if i + 1 < len(words) and words[i + 1][0].isupper():
                    # Multi-word term
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
                "source": "comparison_analysis"
            })
            print(f"🔍 DEBUG: Added comparison card for {terms[0]} vs {terms[1]}")
    
    # Generate cards from process sentences
    for sentence in process_sentences[:num_cards//4]:
        # Extract the main concept
        words = sentence.split()
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2 and word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence']:
                if i + 1 < len(words) and words[i + 1][0].isupper():
                    term = f"{word} {words[i + 1]}"
                else:
                    term = word
                
                flashcards.append({
                    "question": f"How does {term} work?",
                    "answer": sentence,
                    "type": "process",
                    "difficulty": "medium",
                    "source": "process_analysis"
                })
                print(f"🔍 DEBUG: Added process card for {term}")
                break
    
    # Fill remaining cards with concept explanations
    remaining_cards = num_cards - len(flashcards)
    if remaining_cards > 0:
        # Find sentences that explain concepts but weren't used yet
        used_sentences = set(card.get('answer', '') for card in flashcards)
        available_sentences = [s for s in sentences if s not in used_sentences and len(s) > 30]
        
        for sentence in available_sentences[:remaining_cards]:
            # Extract a key concept from the sentence
            words = sentence.split()
            for word in words:
                if (word[0].isupper() and len(word) > 2 and 
                    word.lower() not in ['conversely', 'however', 'while', 'whereas', 'therefore', 'thus', 'hence'] and
                    word not in [card.get('question', '').split()[-1].rstrip('?') for card in flashcards]):
                    
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
                        "source": "context_analysis"
                    })
                    print(f"🔍 DEBUG: Added concept card for {term}")
                    break
    
    print(f"🔍 DEBUG: Generated {len(flashcards)} total cards")
    return flashcards[:num_cards]

@app.get("/")
async def root():
    return {"message": "NOTICAL AI API is running! 🚀"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "NOTICAL AI"}

@app.post("/generate", response_model=FlashcardResponse)
async def generate_flashcards(request: FlashcardRequest):
    """Generate intelligent flashcards based on content analysis"""
    
    try:
        if request.generation_mode == "smart_understanding":
            flashcards = generate_intelligent_flashcards_v2(request.content, request.num_cards)
        else:
            # Fallback to simple generation
            flashcards = generate_intelligent_flashcards_v2(request.content, request.num_cards)
        
        return FlashcardResponse(
            flashcards=flashcards,
            message=f"Generated {len(flashcards)} intelligent flashcards using {request.generation_mode} mode"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flashcard generation failed: {str(e)}")

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "status": "success",
        "message": "API is working!",
        "endpoints": ["/", "/health", "/generate", "/test"]
    }

if __name__ == "__main__":
    print("🚀 Starting NOTICAL AI API on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
