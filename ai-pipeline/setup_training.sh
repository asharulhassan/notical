#!/bin/bash

# 🚀 NOTICALAI-MASTER TRAINING SETUP SCRIPT
# This script automatically sets up the environment for training

echo "🚀 Setting up NoticalAI-Master Training Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "src/ai_training_pipeline.py" ]; then
    echo "❌ Error: Please run this script from the ai-pipeline directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected: .../notical/ai-pipeline/"
    exit 1
fi

echo "✅ Confirmed: Running from correct directory"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "🐍 Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if all training data exists
echo "🔍 Verifying training data..."
training_files=(
    "generated_flashcards/massive_english_training.json"
    "generated_flashcards/massive_humanities_training.json"
    "generated_flashcards/massive_complex_subjects_training.json"
    "generated_flashcards/massive_english_testing.json"
    "generated_flashcards/massive_humanities_testing.json"
    "generated_flashcards/massive_complex_subjects_testing.json"
)

missing_files=0
for file in "${training_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ Missing: $file"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    echo "❌ Error: $missing_files training files are missing!"
    echo "   Please ensure all data files are present before training."
    exit 1
fi

# Check system resources
echo "💻 Checking system resources..."
echo "   CPU cores: $(nproc)"
echo "   Memory: $(free -h | awk 'NR==2{printf "%.1f GB", $2/1024}')"
echo "   Available memory: $(free -h | awk 'NR==2{printf "%.1f GB", $7/1024}')"

# Check for GPU
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU detected: NVIDIA"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | while IFS=, read -r name memory; do
        echo "   GPU: $name, Memory: ${memory}MB"
    done
else
    echo "💻 No NVIDIA GPU detected - will use CPU training"
fi

# Create training directory
mkdir -p training_outputs
echo "📁 Created training_outputs directory"

echo ""
echo "🎉 SETUP COMPLETE! You're ready to train your AI model."
echo ""
echo "🚀 To start training, run:"
echo "   python src/ai_training_pipeline.py"
echo ""
echo "📊 Training will create:"
echo "   - trained_model.json (model weights)"
echo "   - training_report.txt (performance summary)"
echo "   - training_outputs/ (additional logs)"
echo ""
echo "⏱️  Expected training time: 2-6 hours on powerful machine"
echo "💾 Ensure you have at least 8GB free RAM and stable power supply"
echo ""
echo "📖 For detailed instructions, see: TRAINING_CONTEXT.md"
echo "=================================================="
