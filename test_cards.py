#!/usr/bin/env python3
"""
Test script to see generated flashcards
"""
import sys
sys.path.append('ai-pipeline')

from core.self_learning_llm import SelfLearningLLM

def test_cards():
    print("Testing flashcard generation...")
    llm = SelfLearningLLM()
    
    content = "Python is a programming language."
    cards = llm.generate_flashcards(content, 2)
    
    print(f"\nGenerated {len(cards)} cards:")
    for i, card in enumerate(cards, 1):
        print(f"\nCard {i}:")
        print(f"Q: {card['question']}")
        print(f"A: {card['answer']}")
        print(f"Context: {card['content_context']}")

if __name__ == "__main__":
    test_cards()
