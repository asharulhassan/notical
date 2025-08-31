#!/usr/bin/env python3
"""
NOTICAL Enterprise Startup Script
Tests the system and starts the production API
"""

import os
import sys
import subprocess
import time

def print_header():
    print("🚀" + "="*70)
    print("🚀                    NOTICAL ENTERPRISE SYSTEM                    🚀")
    print("🚀" + "="*70)
    print()

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing NOTICAL Enterprise Setup...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CUDA not available")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    # Test our custom modules
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from core.self_learning_llm import SelfLearningLLM
        print("✅ SelfLearningLLM import successful")
    except ImportError as e:
        print(f"❌ SelfLearningLLM import failed: {e}")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📁 Python path: {sys.path}")
        return False
    
    try:
        from training.continuous_learning import ContinuousLearningPipeline
        print("✅ ContinuousLearningPipeline import successful")
    except ImportError as e:
        print(f"❌ ContinuousLearningPipeline import failed: {e}")
        return False
    
    try:
        from core.enhanced_ai_core import EnhancedNOTICALAICore
        print("✅ EnhancedNOTICALAICore import successful")
    except ImportError as e:
        print(f"❌ EnhancedNOTICALAICore import failed: {e}")
        return False
    
    print("✅ All enterprise components imported successfully!")
    return True

def test_llm_creation():
    """Test if we can create an LLM instance"""
    print("\n🧠 Testing Enterprise LLM Creation...")
    
    try:
        from core.self_learning_llm import SelfLearningLLM
        
        # Create LLM instance (this will download/load the model)
        print("🔄 Creating Enterprise LLM instance...")
        llm = SelfLearningLLM()
        
        print("✅ Enterprise LLM created successfully!")
        print(f"📍 Device: {llm.device}")
        print(f"📁 Model: {llm.model_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enterprise LLM creation failed: {e}")
        return False

def main():
    print_header()
    
    print("🎯 This script will:")
    print("   1. Test your Python environment")
    print("   2. Test the enterprise LLM components")
    print("   3. Start the NOTICAL Enterprise API")
    print()
    
    # Step 1: Test Python environment
    print("🧪 STEP 1: Testing Python Environment")
    print("=" * 60)
    
    if not test_imports():
        print("\n❌ Setup test failed - imports not working")
        print("💡 You may need to install dependencies:")
        print("   pip install -r requirements.txt")
        return
    
    # Step 2: Test LLM creation
    print("\n🧪 STEP 2: Testing Enterprise LLM")
    print("=" * 60)
    
    if not test_llm_creation():
        print("\n❌ LLM test failed - cannot create LLM instance")
        return
    
    print("✅ All enterprise tests passed!")
    
    # Step 3: Start the enterprise server
    print("\n🚀 STEP 3: Starting NOTICAL Enterprise API")
    print("=" * 60)
    
    print("🎯 The enterprise system will start in 3 seconds...")
    print("📡 Server will be available at: http://localhost:8004")
    print("🌐 API docs will be at: http://localhost:8004/docs")
    print("📊 System health at: http://localhost:8004/")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    for i in range(3, 0, -1):
        print(f"⏰ Starting in {i}...")
        time.sleep(1)
    
    print("🚀 Starting NOTICAL Enterprise System...")
    
    # Start the enterprise server
    try:
        subprocess.run(
            "python main.py",
            shell=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except KeyboardInterrupt:
        print("\n⏹️  Enterprise server stopped by user")
    except Exception as e:
        print(f"❌ Enterprise server failed to start: {e}")

if __name__ == "__main__":
    main()
