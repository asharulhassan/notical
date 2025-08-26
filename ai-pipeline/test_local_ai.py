#!/usr/bin/env python3
"""
Test script for the local AI flashcard pipeline
"""

import sys
import os
sys.path.append('app')

from workers.flashcard_worker import FlashcardWorker
import asyncio

async def test_local_ai():
    """Test the local AI pipeline"""
    
    print("🧠 Testing Local AI Flashcard Pipeline")
    print("=" * 50)
    
    # Sample content
    sample_content = """
    Photosynthesis is the process by which plants convert sunlight into energy. 
    This process occurs in the chloroplasts and involves two main stages: 
    light-dependent reactions and light-independent reactions. The light-dependent 
    reactions capture solar energy and convert it to chemical energy, while the 
    light-independent reactions use this energy to synthesize glucose from carbon dioxide.
    """
    
    print(f"📝 Sample Content: {sample_content.strip()}")
    print()
    
    # Initialize worker
    worker = FlashcardWorker()
    
    # Test different card types
    card_types = ['definition', 'cloze', 'explanation']
    
    print("🎯 Generating flashcards with local AI...")
    print()
    
    try:
        flashcards = await worker.generate_flashcards(
            content=sample_content,
            subject="Biology",
            card_types=card_types,
            num_cards=6,
            difficulty_balance="balanced"
        )
        
        print(f"✅ Generated {len(flashcards)} flashcards!")
        print()
        
        for i, card in enumerate(flashcards, 1):
            print(f"📚 Card {i} ({card['card_type'].upper()})")
            print(f"   Question: {card['question']}")
            print(f"   Answer: {card['answer']}")
            print(f"   Hint: {card['hint']}")
            print(f"   Difficulty: {card['difficulty']}")
            print(f"   Confidence: {card['confidence_score']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_local_ai())
