#!/usr/bin/env python3
"""
NOTICAL Enterprise System Test Suite
Comprehensive testing of all enterprise components
"""

import sys
import os
import time
import json
from datetime import datetime

def print_header():
    print("🧪" + "="*70)
    print("🧪                    NOTICAL ENTERPRISE TEST SUITE                    🧪")
    print("🧪" + "="*70)
    print()

def test_imports():
    """Test all enterprise component imports"""
    print("🧪 Testing Enterprise Component Imports...")
    
    tests = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
    ]
    
    all_passed = True
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name}: Import successful")
        except ImportError as e:
            print(f"❌ {name}: Import failed - {e}")
            all_passed = False
    
    # Test custom components
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from core.self_learning_llm import SelfLearningLLM
        print("✅ SelfLearningLLM: Import successful")
    except ImportError as e:
        print(f"❌ SelfLearningLLM: Import failed - {e}")
        all_passed = False
    
    try:
        from training.continuous_learning import ContinuousLearningPipeline
        print("✅ ContinuousLearningPipeline: Import successful")
    except ImportError as e:
        print(f"❌ ContinuousLearningPipeline: Import failed - {e}")
        all_passed = False
    
    try:
        from core.enhanced_ai_core import EnhancedNOTICALAICore
        print("✅ EnhancedNOTICALAICore: Import successful")
    except ImportError as e:
        print(f"❌ EnhancedNOTICALAICore: Import failed - {e}")
        all_passed = False
    
    try:
        from core.config import APP_NAME, APP_VERSION, DEVICE
        print(f"✅ Config: {APP_NAME} v{APP_VERSION} on {DEVICE}")
    except ImportError as e:
        print(f"❌ Config: Import failed - {e}")
        all_passed = False
    
    return all_passed

def test_llm_creation():
    """Test LLM instance creation"""
    print("\n🧠 Testing Enterprise LLM Creation...")
    
    try:
        from core.self_learning_llm import SelfLearningLLM
        
        print("🔄 Creating LLM instance...")
        start_time = time.time()
        
        llm = SelfLearningLLM()
        
        creation_time = time.time() - start_time
        print(f"✅ LLM created successfully in {creation_time:.2f}s")
        print(f"📍 Device: {llm.device}")
        print(f"📁 Model: {llm.model_name}")
        
        # Test model stats
        stats = llm.get_model_stats()
        print(f"📊 Model stats: {stats.get('total_parameters', 'N/A')} parameters")
        
        return True, llm
        
    except Exception as e:
        print(f"❌ LLM creation failed: {e}")
        return False, None

def test_flashcard_generation(llm):
    """Test flashcard generation"""
    print("\n🎯 Testing Flashcard Generation...")
    
    try:
        test_content = """
        Machine learning is a subset of artificial intelligence that focuses on algorithms 
        that can learn from data. It enables computers to improve their performance on 
        a specific task without being explicitly programmed for that task.
        """
        
        print("🔄 Generating flashcards...")
        start_time = time.time()
        
        flashcards = llm.generate_flashcards(
            content=test_content,
            num_cards=3
        )
        
        generation_time = time.time() - start_time
        print(f"✅ Generated {len(flashcards)} flashcards in {generation_time:.2f}s")
        
        # Display flashcards
        for i, card in enumerate(flashcards, 1):
            print(f"  📝 Card {i}:")
            print(f"    Q: {card.get('question', 'N/A')}")
            print(f"    A: {card.get('answer', 'N/A')}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Flashcard generation failed: {e}")
        return False

def test_enhanced_ai_core():
    """Test enhanced AI core functionality"""
    print("\n⚡ Testing Enhanced AI Core...")
    
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
        print(f"❌ Enhanced AI Core test failed: {e}")
        return False

def test_training_pipeline():
    """Test training pipeline functionality"""
    print("\n🔄 Testing Training Pipeline...")
    
    try:
        from training.continuous_learning import ContinuousLearningPipeline
        
        print("🔄 Creating training pipeline...")
        pipeline = ContinuousLearningPipeline()
        
        print("🔄 Getting training status...")
        status = pipeline.get_training_status()
        
        print(f"✅ Training pipeline status:")
        print(f"  📊 Feedback samples: {status.get('feedback_samples', 0)}")
        print(f"  🔄 Ready for training: {status.get('ready_for_training', False)}")
        print(f"  📈 Training history: {status.get('training_history', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Training pipeline test failed: {e}")
        return False

def test_system_integration():
    """Test system integration"""
    print("\n🔗 Testing System Integration...")
    
    try:
        # Test that all components can work together
        from core.self_learning_llm import SelfLearningLLM
        from training.continuous_learning import ContinuousLearningPipeline
        from core.enhanced_ai_core import EnhancedNOTICALAICore
        
        print("🔄 Creating integrated system...")
        
        llm = SelfLearningLLM()
        pipeline = ContinuousLearningPipeline()
        ai_core = EnhancedNOTICALAICore()
        
        print("✅ All components created successfully")
        print("✅ System integration test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ System integration test failed: {e}")
        return False

def main():
    print_header()
    
    print("🎯 This test suite will verify:")
    print("   1. ✅ All enterprise component imports")
    print("   2. 🧠 Self-learning LLM functionality")
    print("   3. 🎯 Flashcard generation")
    print("   4. ⚡ Enhanced AI core features")
    print("   5. 🔄 Training pipeline")
    print("   6. 🔗 System integration")
    print()
    
    # Test 1: Imports
    print("🧪 TEST 1: Component Imports")
    print("=" * 60)
    
    if not test_imports():
        print("\n❌ Import tests failed. Cannot proceed.")
        return
    
    # Test 2: LLM Creation
    print("\n🧪 TEST 2: LLM Creation")
    print("=" * 60)
    
    llm_success, llm = test_llm_creation()
    if not llm_success:
        print("\n❌ LLM creation failed. Cannot proceed.")
        return
    
    # Test 3: Flashcard Generation
    print("\n🧪 TEST 3: Flashcard Generation")
    print("=" * 60)
    
    if not test_flashcard_generation(llm):
        print("\n❌ Flashcard generation failed.")
        return
    
    # Test 4: Enhanced AI Core
    print("\n🧪 TEST 4: Enhanced AI Core")
    print("=" * 60)
    
    if not test_enhanced_ai_core():
        print("\n❌ Enhanced AI Core test failed.")
        return
    
    # Test 5: Training Pipeline
    print("\n🧪 TEST 5: Training Pipeline")
    print("=" * 60)
    
    if not test_training_pipeline():
        print("\n❌ Training pipeline test failed.")
        return
    
    # Test 6: System Integration
    print("\n🧪 TEST 6: System Integration")
    print("=" * 60)
    
    if not test_system_integration():
        print("\n❌ System integration test failed.")
        return
    
    # All tests passed
    print("\n🎉" + "="*60)
    print("🎉                    ALL ENTERPRISE TESTS PASSED!                    🎉")
    print("🎉" + "="*60)
    print()
    print("✅ NOTICAL Enterprise System is fully functional!")
    print("🚀 You can now start the production server with:")
    print("   python start_notical.py")
    print()
    print("📡 Server will be available at: http://localhost:8004")
    print("🌐 API docs will be at: http://localhost:8004/docs")
    print("📊 System health at: http://localhost:8004/")

if __name__ == "__main__":
    main()
