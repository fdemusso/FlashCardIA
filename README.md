# 🎯 AI Flashcard Generator

A modern web application that generates personalized educational flashcards from PDF documents using local artificial intelligence (Ollama with Gemma model). The system has been designed with modular architecture in both backend and frontend to ensure scalability and maintainability.

## ✨ Key Features

### 🤖 Advanced AI Generation
- **3 types of questions**: Multiple choice, True/False, Open-ended questions
- **Automatic explanations**: Detailed explanations for each answer
- **Intelligent validation**: Fallback system to ensure response consistency
- **Difficulty scoring**: Each flashcard has a difficulty level from 1 to 5

### 🏗️ Modular Architecture
- **Modularized backend**: Separation into services (`ai_service`, `models`, `validation`)
- **Frontend with custom hooks**: Business logic separated from UI
- **Reusable components**: Scalable and maintainable architecture
- **Complete type safety**: TypeScript to reduce runtime errors

### 🎨 Modern User Interface
- **Responsive design**: Optimized for every device
- **Progress tracking**: Progress bar during processing
- **Visual feedback**: Clear indicators for correct/incorrect answers
- **Intuitive navigation**: Simple and accessible controls

## 📋 System Requirements

### Required Software
- **Python** 3.8 or higher
- **Node.js** 16 or higher  
- **Ollama** (latest version)
- **Git** (for repository cloning)

### AI Model
The project uses Ollama's `gemma3:4b-it-qat` model, optimized for Italian.

## 🚀 Quick Installation

### 1. Ollama Setup
```bash
# Install Ollama from https://ollama.ai/
# Then download the model:
ollama pull gemma3:4b-it-qat
```

### 2. Clone and Backend Setup
```bash
git clone <repository-url>
cd "IA flashcard"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend
cd backend
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
# In a new terminal window
cd frontend
npm install
npm start
```

## 🎮 How to Use

1. **Check prerequisites**: Make sure Ollama is running with the correct model
2. **Access the app**: Open `http://localhost:3000` in your browser
3. **Upload PDF**: Select a PDF document (max 10MB)
4. **Wait for processing**: The system processes the document and generates flashcards
5. **Study**: Navigate through flashcards and test your knowledge

## 🏛️ Project Architecture

### Complete Structure
```
IA flashcard/
├── backend/                 # Python FastAPI API
│   ├── main.py             # Entry point and routing
│   ├── ai_service.py       # AI generation logic
│   ├── models.py           # Pydantic data models  
│   ├── validation.py       # Response validation
│   ├── pdf_processor.py    # PDF processing
│   └── config.py           # Application configuration
├── frontend/               # React Application
│   ├── public/             # Static files
│   └── src/
│       ├── components/
│       │   ├── FlashcardViewer/  # Flashcard visualization
│       │   ├── FileUpload/       # Upload management
│       │   ├── Statistics/       # Document statistics
│       │   └── common/           # Shared components
│       ├── hooks/          # Custom hooks business logic
│       ├── services/       # API and external services
│       ├── types/          # TypeScript interfaces
│       ├── utils/          # Utility and helper functions
│       └── App.tsx         # Main orchestrator
├── docs/                   # Project documentation
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
├── package.json           # Node.js configuration
└── README.md              # This file
```

## 🧪 Testing and Verification

### Health Check
```bash
curl http://localhost:8000/health
```

### Component Testing
```bash
# Backend
cd backend
python -m pytest

# Frontend  
cd frontend
npm test
```

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **Ollama not responding** | Verify the service is running: `ollama list` |
| **Model not found** | Download the model: `ollama pull gemma3:4b-it-qat` |
| **CORS errors** | Make sure frontend is on port 3000 |
| **PDF too large** | 10MB limit, reduce file size |
| **Processing timeout** | Complex files require more time |

### Logs and Debug
- **Backend logs**: Console where `uvicorn` is running
- **Frontend logs**: Browser DevTools (F12)
- **Ollama logs**: `ollama logs`

## 📈 Roadmap and Contributions

### Upcoming Features
- [ ] Export flashcards to external formats
- [ ] Spaced repetition system
- [ ] Support for multiple AI models
- [x] Complete offline mode
- [ ] Learning analytics

### How to Contribute
1. **Fork** the repository
2. **Create branch** for feature: `git checkout -b feature/feature-name`
3. **Commit** changes: `git commit -m 'Add new feature'`
4. **Push** to branch: `git push origin feature/feature-name`
5. **Open Pull Request**

## 📊 Versioning

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

- **v3.0**: Complete frontend refactoring with modular architecture
- **v2.1**: Multiple choice response consistency fix
- **v2.0**: Added automatic explanations
- **v1.0**: Initial release

## 📝 License

This project is released under **MIT license**. See [LICENSE](LICENSE) for details.

---

⭐ **If this project is useful to you, leave a star on GitHub!** 