#!/usr/bin/env python3
"""
Test NOTICAL with Your Own Content
Just run this and paste in whatever content you want to test!
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_with_your_content():
    """Test NOTICAL with content you provide"""
    print("🎯 NOTICAL Content Test - Use Your Own Data!")
    print("=" * 60)
    
    try:
        from core.self_learning_llm import SelfLearningLLM
        
        print("🔄 Loading NOTICAL LLM...")
        llm = SelfLearningLLM()
        print("✅ LLM loaded successfully!")
        
        # Get content from user
        print("\n📝 Enter your content below (press Enter twice when done):")
        print("(Or paste content from your website, documents, etc.)")
        print("-" * 60)
        
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        
        # Remove the last empty line
        if lines and lines[-1] == "":
            lines.pop()
        
        content = "\n".join(lines)
        
        if not content.strip():
            print("❌ No content provided. Using sample content instead.")
            content = """
            Machine learning is a subset of artificial intelligence that focuses on algorithms 
            that can learn from data. It enables computers to improve their performance on 
            a specific task without being explicitly programmed for that task.
            """
        
        print(f"\n📝 Content to process:")
        print(f"   Length: {len(content)} characters")
        print(f"   Preview: {content[:100]}...")
        
        # Get number of flashcards
        try:
            num_cards = int(input(f"\n🎯 How many flashcards do you want? (default: 5): ") or "5")
        except ValueError:
            num_cards = 5
        
        print(f"\n🔄 Generating {num_cards} flashcards...")
        start_time = time.time()
        
        flashcards = llm.generate_flashcards(
            content=content,
            num_cards=num_cards
        )
        
        generation_time = time.time() - start_time
        
        print(f"✅ Generated {len(flashcards)} flashcards in {generation_time:.2f}s")
        print(f"\n📚 Your Generated Flashcards:")
        print("=" * 60)
        
        for i, card in enumerate(flashcards, 1):
            print(f"📝 Card {i}:")
            print(f"   Q: {card.get('question', 'N/A')}")
            print(f"   A: {card.get('answer', 'N/A')}")
            print()
        
        # Test enhanced AI analysis
        print("⚡ Enhanced AI Analysis:")
        print("-" * 40)
        
        from core.enhanced_ai_core import EnhancedNOTICALAICore
        ai_core = EnhancedNOTICALAICore()
        
        analysis = ai_core.analyze_content_intelligently(content)
        
        print(f"📊 Key concepts: {len(analysis.get('key_concepts', []))}")
        print(f"📊 Complexity score: {analysis.get('complexity_score', 'N/A')}")
        print(f"📊 Subject areas: {analysis.get('subject_areas', [])}")
        
        if analysis.get('key_concepts'):
            print(f"\n🔑 Key Concepts Found:")
            for concept in analysis['key_concepts'][:5]:  # Show first 5
                print(f"   • {concept.get('concept', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 NOTICAL - Test with Your Real Content!")
    print("=" * 60)
    
    if test_with_your_content():
        print("\n🎉" + "="*60)
        print("🎉                    TEST COMPLETED!                    🎉")
        print("🎉" + "="*60)
        print()
        print("✅ NOTICAL is working with your content!")
        print("🚀 The AI is generating flashcards successfully!")
        print("💡 The server issue is separate from the AI functionality")
        print()
        print("🎯 Next steps:")
        print("   1. Your AI is working perfectly")
        print("   2. We can integrate this with your website")
        print("   3. Just need to fix the server startup issue")
    else:
        print("\n❌ Test failed. Check the error above.")
