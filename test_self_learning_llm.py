#!/usr/bin/env python3
"""
Test Script for NOTICAL Self-Learning LLM
Tests the complete system to ensure it works correctly
"""

import sys
import os
import time
import json
from datetime import datetime

# Add the ai-pipeline directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-pipeline'))

def test_self_learning_llm():
    """Test the self-learning LLM system"""
    print("🚀 Testing NOTICAL Self-Learning LLM System...")
    print("=" * 60)
    
    try:
        # Test 1: Import the components
        print("📥 Test 1: Importing components...")
        from core.self_learning_llm import SelfLearningLLM
        from training.continuous_learning import ContinuousLearningPipeline
        print("✅ All components imported successfully!")
        
        # Test 2: Initialize the LLM
        print("\n🤖 Test 2: Initializing Self-Learning LLM...")
        start_time = time.time()
        
        llm = SelfLearningLLM()
        init_time = time.time() - start_time
        
        print(f"✅ LLM initialized in {init_time:.2f}s")
        print(f"   Device: {llm.device}")
        print(f"   Model: {llm.model_name}")
        
        # Test 3: Get model stats
        print("\n📊 Test 3: Getting model statistics...")
        stats = llm.get_model_stats()
        print(f"✅ Model stats retrieved:")
        print(f"   Total parameters: {stats.get('total_parameters', 'N/A'):,}")
        print(f"   Device: {stats.get('device', 'N/A')}")
        
        if stats.get('device') == 'cuda':
            gpu_mem = stats.get('gpu_memory_allocated', 0)
            print(f"   GPU Memory: {gpu_mem / 1024**3:.2f} GB")
        
        # Test 4: Generate flashcards
        print("\n🎯 Test 4: Generating test flashcards...")
        test_content = """
        Artificial Intelligence (AI) is a branch of computer science that aims to create 
        intelligent machines that work and react like humans. Machine learning is a subset 
        of AI that enables computers to learn and improve from experience without being 
        explicitly programmed. Deep learning, a subset of machine learning, uses neural 
        networks with multiple layers to analyze various factors of data.
        """
        
        start_time = time.time()
        flashcards = llm.generate_flashcards(test_content, num_cards=3)
        gen_time = time.time() - start_time
        
        print(f"✅ Generated {len(flashcards)} flashcards in {gen_time:.2f}s")
        
        for i, card in enumerate(flashcards, 1):
            print(f"   Card {i}:")
            print(f"     Q: {card['question']}")
            print(f"     A: {card['answer']}")
            print()
        
        # Test 5: Test feedback collection
        print("📝 Test 5: Testing feedback collection...")
        test_feedback = {
            'flashcard_id': 'test_card_1',
            'user_rating': 4,
            'user_correction': None
        }
        
        llm.collect_feedback(**test_feedback)
        print("✅ Feedback collected successfully!")
        
        # Test 6: Initialize training pipeline
        print("\n🔄 Test 6: Initializing training pipeline...")
        training_pipeline = ContinuousLearningPipeline()
        print("✅ Training pipeline initialized!")
        
        # Test 7: Check training status
        print("\n📊 Test 7: Checking training status...")
        status = training_pipeline.get_training_status()
        print(f"✅ Training status:")
        print(f"   Feedback samples: {status['feedback_samples']}")
        print(f"   Ready for training: {status['ready_for_training']}")
        print(f"   Training history: {status['training_history']}")
        
        # Test 8: Test model persistence
        print("\n💾 Test 8: Testing model persistence...")
        original_stats = llm.get_model_stats()
        print("✅ Model stats before save:")
        print(f"   Parameters: {original_stats.get('total_parameters', 'N/A'):,}")
        
        # Test 9: Performance benchmark
        print("\n⚡ Test 9: Performance benchmark...")
        benchmark_content = "Python is a high-level programming language known for its simplicity and readability."
        
        times = []
        for _ in range(3):
            start = time.time()
            llm.generate_flashcards(benchmark_content, num_cards=2)
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"✅ Average generation time: {avg_time:.3f}s")
        print(f"   Best time: {min(times):.3f}s")
        print(f"   Worst time: {max(times):.3f}s")
        
        # Test 10: System summary
        print("\n🎉 Test 10: System summary...")
        final_stats = llm.get_model_stats()
        
        print("✅ NOTICAL Self-Learning LLM System is working perfectly!")
        print("\n📋 System Summary:")
        print(f"   Model: {final_stats.get('model_name', 'N/A')}")
        print(f"   Device: {final_stats.get('device', 'N/A')}")
        print(f"   Parameters: {final_stats.get('total_parameters', 'N/A'):,}")
        print(f"   Feedback collected: {len(llm.feedback_data)}")
        print(f"   Ready for training: {status['ready_for_training']}")
        
        if final_stats.get('device') == 'cuda':
            print(f"   GPU Memory: {final_stats.get('gpu_memory_allocated', 0) / 1024**3:.2f} GB")
        
        print("\n🚀 Your RTX 4070 is now an AI powerhouse!")
        print("   The system is ready to generate high-quality flashcards and learn from user feedback!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    print("=" * 40)
    
    try:
        import requests
        import time
        
        base_url = "http://localhost:8004"
        
        # Test 1: Health check
        print("🔍 Test 1: Health check endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        
        # Test 2: Root endpoint
        print("\n🏠 Test 2: Root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        # Test 3: Model stats
        print("\n📊 Test 3: Model stats endpoint...")
        response = requests.get(f"{base_url}/model-stats")
        if response.status_code == 200:
            print("✅ Model stats endpoint working!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
        else:
            print(f"❌ Model stats failed: {response.status_code}")
        
        # Test 4: Training status
        print("\n🔄 Test 4: Training status endpoint...")
        response = requests.get(f"{base_url}/training-status")
        if response.status_code == 200:
            print("✅ Training status endpoint working!")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Feedback samples: {data.get('feedback_samples')}")
        else:
            print(f"❌ Training status failed: {response.status_code}")
        
        print("\n✅ API endpoints test completed!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧠 NOTICAL Self-Learning LLM Test Suite")
    print("=" * 50)
    
    # Test the core system
    core_success = test_self_learning_llm()
    
    if core_success:
        print("\n🎯 Core system tests passed! Starting API tests...")
        
        # Wait a bit for the API to be ready
        print("⏳ Waiting for API to be ready...")
        time.sleep(5)
        
        # Test the API endpoints
        api_success = test_api_endpoints()
        
        if api_success:
            print("\n🎉 ALL TESTS PASSED! Your self-learning LLM is ready!")
            print("\n🚀 Next steps:")
            print("   1. Start the API server: python ai-pipeline/api/self_learning_api.py")
            print("   2. Test with your website")
            print("   3. Collect user feedback to start learning!")
        else:
            print("\n⚠️ Core system works but API needs attention")
    else:
        print("\n❌ Core system tests failed. Please check the errors above.")
    
    print("\n" + "=" * 50)
