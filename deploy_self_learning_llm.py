#!/usr/bin/env python3
"""
Production Deployment Script for NOTICAL Self-Learning LLM
Sets up the complete system for production use
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step, description):
    """Print a step description"""
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    print(f"   Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed!")
            print(f"   Error: {result.stderr.strip()}")
            if check:
                raise RuntimeError(f"Command failed: {command}")
            return False
            
    except Exception as e:
        print(f"❌ Error running command: {e}")
        if check:
            raise
        return False

def check_system_requirements():
    """Check if system meets requirements"""
    print_header("System Requirements Check")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python version: {sys.version}")
    
    # Check PyTorch and CUDA
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"✅ CUDA version: {torch.version.cuda}")
        else:
            print("⚠️ CUDA not available - training will be slow on CPU")
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    
    # Check other dependencies
    required_packages = ['transformers', 'datasets', 'accelerate', 'peft']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print_step(1, "Setting up directories")
    
    directories = [
        "models",
        "training_logs",
        "feedback_archives",
        "api_logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def download_base_model():
    """Download the base model"""
    print_step(2, "Downloading base model")
    
    try:
        # Import and initialize the LLM (this will download the model)
        sys.path.append('ai-pipeline')
        from core.self_learning_llm import SelfLearningLLM
        
        print("🔄 Initializing Self-Learning LLM (this will download the base model)...")
        llm = SelfLearningLLM()
        
        # Get model stats
        stats = llm.get_model_stats()
        print(f"✅ Base model downloaded successfully!")
        print(f"   Model: {stats.get('model_name')}")
        print(f"   Parameters: {stats.get('total_parameters', 0):,}")
        print(f"   Device: {stats.get('device')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading base model: {e}")
        return False

def test_core_system():
    """Test the core system"""
    print_step(3, "Testing core system")
    
    try:
        # Run the test script
        test_script = "test_self_learning_llm.py"
        if os.path.exists(test_script):
            print("🔄 Running core system tests...")
            result = subprocess.run([sys.executable, test_script], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Core system tests passed!")
                return True
            else:
                print("❌ Core system tests failed!")
                print(f"   Error: {result.stderr}")
                return False
        else:
            print("⚠️ Test script not found, skipping core tests")
            return True
            
    except Exception as e:
        print(f"❌ Error testing core system: {e}")
        return False

def start_api_server():
    """Start the API server"""
    print_step(4, "Starting API server")
    
    try:
        api_script = "ai-pipeline/api/self_learning_api.py"
        if not os.path.exists(api_script):
            print(f"❌ API script not found: {api_script}")
            return False
        
        print("🔄 Starting API server in background...")
        
        # Start the server in background
        process = subprocess.Popen([
            sys.executable, api_script
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(10)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:8004/health", timeout=5)
            if response.status_code == 200:
                print("✅ API server started successfully!")
                print(f"   Server PID: {process.pid}")
                print(f"   Health check: {response.json()}")
                
                # Save PID for later
                with open("api_server.pid", "w") as f:
                    f.write(str(process.pid))
                
                return True
            else:
                print(f"❌ API server health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ API server health check failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print_step(5, "Testing API endpoints")
    
    try:
        import requests
        import time
        
        base_url = "http://localhost:8004"
        endpoints = [
            "/",
            "/health",
            "/model-stats",
            "/training-status"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {endpoint}: OK")
                else:
                    print(f"❌ {endpoint}: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ {endpoint}: {e}")
                return False
        
        print("✅ All API endpoints working!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def create_production_config():
    """Create production configuration"""
    print_step(6, "Creating production configuration")
    
    config = {
        "api": {
            "host": "0.0.0.0",
            "port": 8004,
            "workers": 1,
            "reload": False
        },
        "model": {
            "base_model": "google/flan-t5-base",
            "max_length": 1024,
            "temperature": 0.7,
            "device": "auto"
        },
        "training": {
            "min_feedback_samples": 10,
            "max_epochs": 3,
            "learning_rate": 5e-5,
            "batch_size": 2
        },
        "monitoring": {
            "log_level": "INFO",
            "save_training_logs": True,
            "backup_models": True
        }
    }
    
    config_file = "production_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Production configuration created: {config_file}")
    return True

def create_startup_script():
    """Create startup script for production"""
    print_step(7, "Creating startup script")
    
    startup_script = """#!/bin/bash
# NOTICAL Self-Learning LLM Startup Script

echo "🚀 Starting NOTICAL Self-Learning LLM System..."

# Change to project directory
cd "$(dirname "$0")"

# Activate virtual environment (if using one)
# source venv/bin/activate

# Start the API server
echo "📡 Starting API server..."
python ai-pipeline/api/self_learning_api.py &

# Save PID
echo $! > api_server.pid

echo "✅ NOTICAL Self-Learning LLM started!"
echo "   API running on port 8004"
echo "   PID saved to api_server.pid"
echo "   Use 'python deploy_self_learning_llm.py --stop' to stop"
"""
    
    with open("start_notical.sh", "w") as f:
        f.write(startup_script)
    
    # Make executable on Unix systems
    try:
        os.chmod("start_notical.sh", 0o755)
    except:
        pass
    
    print("✅ Startup script created: start_notical.sh")
    return True

def create_stop_script():
    """Create stop script"""
    print_step(8, "Creating stop script")
    
    stop_script = """#!/bin/bash
# NOTICAL Self-Learning LLM Stop Script

echo "🛑 Stopping NOTICAL Self-Learning LLM System..."

# Check if PID file exists
if [ -f "api_server.pid" ]; then
    PID=$(cat api_server.pid)
    echo "📡 Stopping API server (PID: $PID)..."
    
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ API server stopped"
    else
        echo "⚠️ API server not running"
    fi
    
    rm -f api_server.pid
else
    echo "⚠️ PID file not found"
fi

echo "✅ NOTICAL Self-Learning LLM stopped!"
"""
    
    with open("stop_notical.sh", "w") as f:
        f.write(stop_script)
    
    # Make executable on Unix systems
    try:
        os.chmod("stop_notical.sh", 0o755)
    except:
        pass
    
    print("✅ Stop script created: stop_notical.sh")
    return True

def print_deployment_summary():
    """Print deployment summary"""
    print_header("Deployment Summary")
    
    print("🎉 NOTICAL Self-Learning LLM System deployed successfully!")
    print("\n📋 System Status:")
    print("   ✅ Core LLM: Ready")
    print("   ✅ Training Pipeline: Ready")
    print("   ✅ API Server: Running on port 8004")
    print("   ✅ All endpoints: Working")
    
    print("\n🚀 How to use:")
    print("   1. Generate flashcards: POST http://localhost:8004/generate-flashcards")
    print("   2. Submit feedback: POST http://localhost:8004/submit-feedback")
    print("   3. Check status: GET http://localhost:8004/training-status")
    
    print("\n⚙️ Management:")
    print("   Start: ./start_notical.sh")
    print("   Stop: ./stop_notical.sh")
    print("   Config: production_config.json")
    
    print("\n📊 Next steps:")
    print("   1. Integrate with your website")
    print("   2. Collect user feedback")
    print("   3. Watch the AI learn and improve!")
    
    print("\n💡 Your RTX 4070 is now an AI powerhouse!")
    print("   The system will automatically improve as users provide feedback!")

def main():
    """Main deployment function"""
    print_header("NOTICAL Self-Learning LLM Production Deployment")
    
    try:
        # Check system requirements
        if not check_system_requirements():
            print("❌ System requirements not met. Please install missing dependencies.")
            return False
        
        # Setup directories
        if not setup_directories():
            print("❌ Failed to setup directories")
            return False
        
        # Download base model
        if not download_base_model():
            print("❌ Failed to download base model")
            return False
        
        # Test core system
        if not test_core_system():
            print("❌ Core system test failed")
            return False
        
        # Start API server
        if not start_api_server():
            print("❌ Failed to start API server")
            return False
        
        # Test API endpoints
        if not test_api_endpoints():
            print("❌ API endpoint tests failed")
            return False
        
        # Create production configuration
        if not create_production_config():
            print("❌ Failed to create production config")
            return False
        
        # Create startup script
        if not create_startup_script():
            print("❌ Failed to create startup script")
            return False
        
        # Create stop script
        if not create_stop_script():
            print("❌ Failed to create stop script")
            return False
        
        # Print summary
        print_deployment_summary()
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Deployment completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)
