# 🧠 NOTICAL - AI-Powered Flashcard Learning System

> **NOTICAL** is an intelligent flashcard generation system that learns from user feedback and continuously improves its understanding of various subjects.

## 🚀 Features

- **AI-Powered Flashcard Generation**: Creates relevant, context-aware flashcards from text, PDFs, and audio
- **Self-Learning AI**: Continuously improves based on user feedback and corrections
- **Multi-Format Input**: Supports text, PDF documents, and audio files
- **Smart Content Analysis**: Identifies key concepts, definitions, comparisons, and processes
- **User Feedback Integration**: Learns from good/bad flashcards and user corrections
- **Modern Web Interface**: Beautiful, responsive UI with liquid glass design

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   AI Pipeline   │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PyTorch)     │
│                 │    │                 │    │                 │
│  • Website      │    │  • Request      │    │  • Model       │
│  • UI Components│    │  • Routing      │    │  • Training    │
│  • User Input   │    │  • Validation   │    │  • Generation  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **React** - User interface
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations

### Backend
- **FastAPI** - API framework
- **PyTorch** - AI/ML framework
- **Transformers** - Pre-trained models
- **Uvicorn** - ASGI server

### AI Models
- **Base Model**: Flan-T5 or LLaMA-2
- **Fine-tuning**: Custom training pipeline
- **Self-learning**: Continuous improvement

## 📁 Project Structure

```
notical/
├── website/                 # Frontend React application
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── store/         # State management
│   ├── public/            # Static assets
│   └── package.json       # Dependencies
├── ai-pipeline/           # AI backend
│   ├── api/              # FastAPI endpoints
│   ├── core/             # AI core logic
│   ├── training/         # Training pipeline
│   └── models/           # Trained models
├── shared/               # Shared utilities
└── requirements.txt      # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- RTX 4070 or equivalent GPU (recommended)

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/notical.git
cd notical
```

### 2. Setup AI Pipeline
```bash
cd ai-pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Website
```bash
cd website
npm install
npm start
```

### 4. Start AI API
```bash
cd ai-pipeline/api
python main.py
```

## 🧠 AI Training

### Local Training (RTX 4070 Laptop)
```bash
cd ai-pipeline
python training/trainer.py
```

### Training Configuration
- **Model**: Flan-T5 or LLaMA-2
- **Batch Size**: 4-8 (depending on VRAM)
- **Epochs**: 3-5 per training session
- **Learning Rate**: 5e-5

## 📊 API Endpoints

### Flashcard Generation
```bash
POST /generate
{
  "content": "Your text content here",
  "num_cards": 5
}
```

### Training Data
```bash
POST /add_training_data
{
  "content": "Content used for generation",
  "good_cards": [...],
  "bad_cards": [...]
}
```

### User Feedback
```bash
POST /add_feedback
{
  "question": "Flashcard question",
  "user_answer": "User's answer",
  "correct_answer": "Correct answer",
  "rating": 5
}
```

## 🔄 Development Workflow

### Working on Mac
1. Make changes
2. Test locally
3. Commit and push
4. Pull on RTX 4070 laptop

### Working on RTX 4070 Laptop
1. Pull latest changes
2. Train AI models
3. Test improvements
4. Commit and push
5. Pull on Mac

## 🎯 Roadmap

### Phase 1: MVP (Current)
- [x] Basic flashcard generation
- [x] Website interface
- [x] AI pipeline foundation
- [ ] Self-learning implementation
- [ ] User feedback system

### Phase 2: Enhancement
- [ ] Advanced AI training
- [ ] Multi-modal input (PDF, audio)
- [ ] Performance optimization
- [ ] User analytics

### Phase 3: Scale
- [ ] Cloud deployment
- [ ] Multi-user support
- [ ] Advanced features
- [ ] Mobile app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/notical/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/notical/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- **Hugging Face** for pre-trained models
- **PyTorch** for the AI framework
- **FastAPI** for the backend framework
- **React** for the frontend framework

---

**Made with ❤️ by [Your Name]**

*Building the future of AI-powered learning*
