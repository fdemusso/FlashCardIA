# 📚 Complete Documentation - AI Flashcard Generator

## 🏗️ Architecture Overview

This project is divided into two main parts:
- **Backend**: REST API in Python with FastAPI that handles PDF processing and AI flashcard generation
- **Frontend**: React+TypeScript application for the user interface

## 📂 Project Structure

```
IA-flashcard/
├── backend/               # Python FastAPI API
│   ├── main.py           # Entry point and main routing
│   ├── ai_service.py     # Service for flashcard generation with Ollama
│   ├── models.py         # Pydantic/DataClass data models
│   ├── validation.py     # Flashcard validation and cleaning
│   ├── pdf_processor.py  # PDF text extraction and processing
│   └── config.py         # Configurations and constants
├── frontend/             # React Application
│   └── src/
│       ├── App.tsx       # Main component
│       ├── components/   # Reusable React components
│       ├── hooks/        # Custom hooks for business logic
│       ├── services/     # API services and communication
│       ├── types/        # TypeScript definitions
│       └── utils/        # Utility and helper functions
└── docs/                 # Complete documentation
```

## 🔄 Workflow

1. **PDF Upload**: User uploads a PDF file through the interface
2. **Text Extraction**: Backend extracts and cleans text from PDF
3. **AI Generation**: Text is sent to Ollama to generate flashcards
4. **Validation**: Flashcards are validated and corrected
5. **Display**: Frontend presents flashcards interactively

## 📖 Documentation Sections

- [📱 **Frontend**](./frontend.md) - Complete documentation of React components
- [🔧 **Backend**](./backend.md) - API and Python services documentation
- [🚀 **Deploy**](./deployment.md) - Deployment and configuration guide
- [🧪 **Testing**](./testing.md) - Testing and debugging guides
- [🔄 **API**](./api.md) - REST API documentation

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern web framework for Python
- **Ollama**: Local AI service for text generation
- **PyPDF2**: Library for PDF text extraction
- **Pydantic**: Data validation and serialization

### Frontend
- **React**: UI library for JavaScript
- **TypeScript**: Typed superset of JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Hooks**: Pattern for reusable business logic

## 🎯 Main Features

### 🤖 Intelligent AI Generation
- **3 Question Types**: Multiple choice, True/False, Open-ended
- **Automatic Explanations**: Explanations for each answer
- **Robust Validation**: Fallback system for consistency
- **Difficulty Scoring**: Rating from 1 to 5 for each flashcard

### 🎨 Modern Interface
- **Responsive Design**: Works on every device
- **Progress Tracking**: Real-time progress bar
- **Visual Feedback**: Indicators for correct/incorrect answers
- **Fluid Navigation**: Intuitive controls

### 🔧 Modular Architecture
- **Separation of Concerns**: Well-separated backend and frontend
- **Custom Hooks**: Isolated business logic
- **Reusable Components**: DRY and maintainable code
- **Type Safety**: TypeScript to reduce errors

## 🔍 Quick Start

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Ollama Setup**:
   ```bash
   ollama pull gemma3:4b-it-qat
   ```

## 📞 Support

For specific questions, consult the dedicated documentation sections or open an issue on GitHub. 