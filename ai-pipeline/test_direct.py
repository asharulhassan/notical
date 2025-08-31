#!/usr/bin/env python3
"""
Direct Test of NOTICAL LLM - No Server, Just Core Functionality
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_direct_llm():
    """Test the LLM directly without the server"""
    print("🧪 Testing NOTICAL LLM Directly (No Server)")
    print("=" * 60)
    
    try:
        from core.self_learning_llm import SelfLearningLLM
        
        print("🔄 Creating LLM instance...")
        start_time = time.time()
        
        llm = SelfLearningLLM()
        
        creation_time = time.time() - start_time
        print(f"✅ LLM created successfully in {creation_time:.2f}s")
        print(f"📍 Device: {llm.device}")
        print(f"📁 Model: {llm.model_name}")
        
        # Test with real content
        test_content = """
        Machine learning is a subset of artificial intelligence that focuses on algorithms 
        that can learn from data. It enables computers to improve their performance on 
        a specific task without being explicitly programmed for that task.
        
        Deep learning is a subset of machine learning that uses neural networks with multiple 
        layers to model and understand complex patterns in data.
        """
        
        print(f"\n🎯 Testing with real content:")
        print(f"📝 Content length: {len(test_content)} characters")
        print(f"🔄 Generating 5 flashcards...")
        
        generation_start = time.time()
        
        flashcards = llm.generate_flashcards(
            content=test_content,
            num_cards=5
        )
        
        generation_time = time.time() - generation_start
        
        print(f"✅ Generated {len(flashcards)} flashcards in {generation_time:.2f}s")
        print(f"\n📚 Generated Flashcards:")
        print("-" * 50)
        
        for i, card in enumerate(flashcards, 1):
            print(f"📝 Card {i}:")
            print(f"   Q: {card.get('question', 'N/A')}")
            print(f"   A: {card.get('answer', 'N/A')}")
            print()
        
        # Test model stats
        stats = llm.get_model_stats()
        print(f"📊 Model Statistics:")
        print(f"   Total Parameters: {stats.get('total_parameters', 'N/A'):,}")
        print(f"   Device: {stats.get('device', 'N/A')}")
        print(f"   Model Path: {stats.get('model_path', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct LLM test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_ai():
    """Test enhanced AI core directly"""
    print("\n⚡ Testing Enhanced AI Core Directly")
    print("=" * 60)
    
    try:
        from core.enhanced_ai_core import EnhancedNOTICALAICore
        
        print("🔄 Creating Enhanced AI Core...")
        ai_core = EnhancedNOTICALAICore()
        
        test_content = "Deep learning is a subset of machine learning that uses neural networks with multiple layers."
        
        print("🔄 Analyzing content...")
        analysis = ai_core.analyze_content_intelligently(test_content)
        
        print(f"✅ Content analysis successful")
        print(f"📊 Key concepts: {len(analysis.get('key_concepts', []))}")
        print(f"📊 Complexity score: {analysis.get('complexity_score', 'N/A')}")
        print(f"📊 Subject areas: {analysis.get('subject_areas', [])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced AI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 NOTICAL Direct Test - Core Components Only")
    print("=" * 60)
    
    # Test 1: Direct LLM
    if not test_direct_llm():
        print("\n❌ LLM test failed!")
        sys.exit(1)
    
    # Test 2: Enhanced AI
    if not test_enhanced_ai():
        print("\n❌ Enhanced AI test failed!")
        sys.exit(1)
    
    print("\n🎉" + "="*60)
    print("🎉                    DIRECT TESTS PASSED!                    🎉")
    print("🎉" + "="*60)
    print()
    print("✅ NOTICAL core components are working perfectly!")
    print("🚀 The issue is likely with the server startup, not the AI!")
    print()
    print("💡 Next steps:")
    print("   1. The LLM is working - we can generate flashcards!")
    print("   2. The enhanced AI is working - we can analyze content!")
    print("   3. We just need to fix the server startup issue")
    print()
    print("🎯 Let's test with your website data now!")
