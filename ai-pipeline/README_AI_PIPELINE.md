# 🚀 NOTICAL AI Flashcard Pipeline

A **production-ready, intelligent flashcard generation system** that actually works with your content instead of generating the same generic questions.

## ✨ **What Makes This Different**

### 🧠 **Intelligent AI Generation**
- **Context-aware questions** - AI actually analyzes your text content
- **No more template questions** - Every generation is unique to your material
- **Subject-specific prompting** - Physics, Chemistry, Biology, Math, History, etc.
- **Proper cloze cards** - Complete sentences with meaningful blanks
- **Difficulty balancing** - Easy, Medium, Hard with proper distribution

### 🔍 **Content Analysis**
- **Automatic subject detection** from content keywords
- **Key concept extraction** for relevant question generation
- **Content quality assessment** with scoring
- **Duplicate prevention** using content hashing
- **Multi-format support** - PDF, Audio, Text files

### 🗄️ **Professional Database**
- **PostgreSQL/SQLite** support for production/development
- **Content deduplication** to avoid generating the same cards
- **Study progress tracking** with success rates
- **Flashcard organization** in nested folder structures
- **Content source tracking** for audit trails

## 🏗️ **Architecture**

```
app/
├── main.py                 # FastAPI application with endpoints
├── workers/
│   └── flashcard_worker.py # Intelligent AI generation worker
├── prompts/
│   └── flashcard_prompts.py # Subject-specific prompt engineering
├── utils/
│   └── text_processing.py  # PDF, Audio, Text processing
├── db/
│   ├── models.py           # Database models
│   └── database.py         # Database connection
└── tests/                  # Comprehensive test suite
```

## 🚀 **Quick Start**

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Set Environment Variables**
```bash
export OPENAI_API_KEY="your-openai-api-key"
export DATABASE_URL="sqlite:///./notical_flashcards.db"  # or PostgreSQL URL
```

### 3. **Run the Backend**
```bash
cd app
python main.py
```

### 4. **Generate Flashcards**
```bash
# Text input
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your study material here...",
    "subject": "Physics",
    "card_types": ["definition", "cloze", "explanation"],
    "num_cards": 5,
    "difficulty_balance": "balanced"
  }'

# File upload
curl -X POST "http://localhost:8000/generate-from-file" \
  -F "file=@your_document.pdf" \
  -F "subject=Chemistry" \
  -F "card_types=definition,cloze" \
  -F "num_cards=10"
```

## 🎯 **API Endpoints**

### **Generate Flashcards**
- `POST /generate` - Generate from text content
- `POST /generate-from-file` - Generate from uploaded files
- `GET /flashcards` - Retrieve stored flashcards
- `GET /subjects` - Get available subjects

### **Request Parameters**
```json
{
  "content": "Your study material...",
  "subject": "Physics",                    // Optional, auto-detected if not provided
  "card_types": [                          // Choose from available types
    "definition", "explanation", "cloze", 
    "comparison", "analysis"
  ],
  "num_cards": 5,                         // 3-20 cards
  "difficulty_balance": "balanced"        // easy, medium, hard, balanced
}
```

## 🧪 **Card Types**

### **1. Definition Cards**
- **Purpose**: Test understanding of key terms
- **Example**: "What is the definition of photosynthesis?"
- **Best for**: Vocabulary, terminology, concepts

### **2. Explanation Cards**
- **Purpose**: Test understanding of processes
- **Example**: "How does cellular respiration work?"
- **Best for**: Processes, mechanisms, procedures

### **3. Cloze Cards** ⭐ **Fixed!**
- **Purpose**: Fill-in-the-blank with context
- **Example**: "Complete: 'The _____ is the powerhouse of the cell.'"
- **Best for**: Key terms, important concepts

### **4. Comparison Cards**
- **Purpose**: Test analytical thinking
- **Example**: "What are the differences between mitosis and meiosis?"
- **Best for**: Relationships, contrasts, analysis

### **5. Analysis Cards**
- **Purpose**: Test critical thinking
- **Example**: "What are the implications of climate change?"
- **Best for**: Complex topics, implications, applications

## 🔧 **Advanced Features**

### **Subject-Specific Prompting**
Each subject gets specialized instructions:
- **Physics**: Focus on laws, formulas, calculations
- **Chemistry**: Emphasize reactions, structures, bonding
- **Biology**: Living systems, processes, evolution
- **Mathematics**: Problem-solving, theorems, methods
- **History**: Events, causes, consequences, context

### **Content Processing**
- **PDF Extraction**: Multi-page text extraction with OCR fix
- **Audio Processing**: Speech-to-text with noise reduction
- **Text Cleaning**: Remove duplicates, fix formatting
- **Quality Assessment**: Score content for better generation

### **Database Features**
- **Content Hashing**: Prevent duplicate generation
- **Progress Tracking**: Study statistics and success rates
- **Folder Organization**: GoodNotes-style nested structure
- **Content Sources**: Track where cards came from

## 📊 **Quality Control**

### **Validation Rules**
1. **Complete Questions**: No cut-off or incomplete questions
2. **Content Grounding**: All answers must come from source material
3. **Length Limits**: Questions < 100 chars, Answers < 200 chars
4. **Difficulty Distribution**: Proper easy/medium/hard balance
5. **Hint Generation**: Helpful hints for each card

### **Fallback System**
- **Primary**: OpenAI GPT-4 with intelligent prompting
- **Secondary**: Template-based generation with content analysis
- **Validation**: Post-generation quality checks and fixes

## 🎨 **Frontend Integration**

The frontend now includes:
- **Card Type Selection**: Choose which types to generate
- **Difficulty Control**: Set difficulty balance
- **Subject Selection**: Auto-detect or manual selection
- **File Upload**: Support for PDF, Audio, Text files
- **Real-time Preview**: See generated cards before studying
- **Study Mode**: Interactive flashcard studying

## 🚀 **Production Deployment**

### **Docker Setup**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Environment Variables**
```bash
OPENAI_API_KEY=your-api-key
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional
```

### **Scaling**
- **Background Workers**: Celery for async processing
- **Database**: PostgreSQL for production, Redis for caching
- **Load Balancing**: Multiple worker instances
- **Monitoring**: Logging, metrics, health checks

## 🧪 **Testing**

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_utils.py
pytest tests/test_workers.py
pytest tests/test_prompts.py

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🔮 **Future Enhancements**

- **Multi-language Support**: Generate cards in different languages
- **Image-based Cards**: Generate questions from diagrams/charts
- **Spaced Repetition**: Intelligent study scheduling
- **Collaborative Features**: Share and rate flashcards
- **Advanced Analytics**: Learning progress insights
- **Mobile App**: Native iOS/Android applications

## 📝 **Example Output**

### **Input Content**
```
Photosynthesis is the process by which plants convert sunlight into energy. 
This process occurs in the chloroplasts and involves two main stages: 
light-dependent reactions and light-independent reactions.
```

### **Generated Cards**
```json
{
  "flashcards": [
    {
      "question": "What is photosynthesis?",
      "answer": "The process by which plants convert sunlight into energy",
      "hint": "Look for the main definition in the first sentence",
      "card_type": "definition",
      "difficulty": "easy",
      "confidence_score": 0.95
    },
    {
      "question": "Complete: 'Photosynthesis occurs in the _____ of plant cells.'",
      "answer": "chloroplasts",
      "hint": "Find the organelle mentioned in the second sentence",
      "card_type": "cloze",
      "difficulty": "easy",
      "confidence_score": 0.92
    },
    {
      "question": "What are the two main stages of photosynthesis?",
      "answer": "Light-dependent reactions and light-independent reactions",
      "hint": "Look for the stages mentioned in the last sentence",
      "card_type": "explanation",
      "difficulty": "medium",
      "confidence_score": 0.88
    }
  ]
}
```

## 🎉 **Why This Works**

1. **Intelligent Prompting**: Subject-specific instructions for better quality
2. **Content Analysis**: AI actually reads and understands your material
3. **Validation Pipeline**: Multiple quality checks and fixes
4. **Database Storage**: Prevents duplicates and tracks progress
5. **Fallback Systems**: Always generates something useful
6. **User Control**: Choose exactly what types of cards you want

## 🆘 **Troubleshooting**

### **Common Issues**
- **OpenAI API Errors**: Check API key and rate limits
- **File Processing**: Ensure file formats are supported
- **Database Issues**: Check connection strings and permissions
- **Memory Issues**: Large files may need chunking

### **Support**
- Check logs in `app/logs/`
- Verify environment variables
- Test with simple text first
- Use smaller files for initial testing

---

**This is now a professional-grade flashcard system that rivals commercial solutions!** 🚀
