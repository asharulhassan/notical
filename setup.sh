#!/bin/bash

# NOTICAL Project Setup Script
# This script sets up the project on any machine

echo "🚀 NOTICAL Project Setup"
echo "========================"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo "✅ Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "✅ Detected Linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
    echo "✅ Detected Windows"
else
    OS="unknown"
    echo "⚠️  Unknown OS: $OSTYPE"
fi

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Python3 found"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Python found"
else
    echo "❌ Python not found. Please install Python 3.9+"
    exit 1
fi

# Check if Node.js is installed
if command -v node &> /dev/null; then
    echo "✅ Node.js found: $(node --version)"
else
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Check if npm is installed
if command -v npm &> /dev/null; then
    echo "✅ npm found: $(npm --version)"
else
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo ""
echo "🔧 Setting up AI Pipeline..."

# Setup AI Pipeline
cd ai-pipeline

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
if [[ "$OS" == "windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for GPU support
echo "🔍 Checking GPU support..."
$PYTHON_CMD -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU count: {torch.cuda.device_count()}')" 2>/dev/null || echo "⚠️  PyTorch not installed or error occurred"

cd ..

echo ""
echo "🌐 Setting up Website..."

# Setup Website
cd website

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 To start development:"
echo ""
echo "1. Start AI Pipeline:"
echo "   cd ai-pipeline"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   cd api"
echo "   python main.py"
echo ""
echo "2. Start Website (in new terminal):"
echo "   cd website"
echo "   npm start"
echo ""
echo "3. Open browser:"
echo "   Website: http://localhost:3000"
echo "   AI API: http://localhost:8001"
echo ""
echo "�� Happy coding! 🚀"
