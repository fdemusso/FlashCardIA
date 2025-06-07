# 🔧 Backend Documentation

## 📋 Overview

The backend is developed in Python using FastAPI, providing REST APIs for PDF document processing and flashcard generation through local artificial intelligence (Ollama).

## 🏗️ Architecture

### Main Components

- **main.py**: Application entry point and routing
- **ai_service.py**: Service for AI-powered flashcard generation
- **models.py**: Data models and structures
- **validation.py**: Validation and cleaning of generated flashcards
- **pdf_processor.py**: Text extraction and processing from PDFs
- **config.py**: Application configurations and constants

## 📄 File-by-File Documentation

### 🚀 main.py - Application Entry Point

**Purpose**: Handles main routing and service orchestration.

**Main Endpoints**:
- `POST /upload-pdf`: Processes PDF files and generates flashcards
- `GET /health`: Checks application and service status

**Dependencies**:
- FastAPI for web framework
- CORS middleware for frontend communication
- StreamingResponse for real-time progress

### 🤖 ai_service.py - AI Service

**Purpose**: Manages interaction with Ollama for flashcard generation.

**Main Functions**:
- `generate_flashcards_from_text()`: Generates flashcards from text using AI
- `clean_json_response()`: Cleans and validates JSON responses from AI
- `check_ollama_availability()`: Verifies Ollama service availability

**Features**:
- Prompt engineering optimized for Italian
- Robust handling of JSON parsing errors
- Fallback system for malformed responses

### 📊 models.py - Data Models

**Purpose**: Defines data structures used in the application.

**Classes**:
- `TextChunk`: Represents a portion of text extracted from PDF
- `FlashcardData`: Structure for flashcard data
- `PDFStatistics`: Document processing statistics
- `ProcessingProgress`: Processing progress information

### ✅ validation.py - Flashcard Validation

**Purpose**: Validates and corrects AI-generated flashcards.

**Functions**:
- `validate_flashcards()`: Validates a list of flashcards

**Checks Performed**:
- Verifies required fields
- Validates question types
- Checks multiple choice option consistency
- Manages answer indices
- Cleans texts and formatting

### 📑 pdf_processor.py - PDF Processing

**Purpose**: Extracts and processes text from PDF documents.

**Functions**:
- `extract_text_from_pdf()`: Extracts text page by page
- `clean_text()`: Cleans text from unwanted characters
- `merge_chunks_intelligently()`: Groups text into optimal portions

**Features**:
- Automatic text cleaning
- Robust handling of reading errors
- Optimization for AI processing

### ⚙️ config.py - Configurations

**Purpose**: Centralizes all application configurations.

**Categories**:
- CORS and networking configurations
- AI model parameters (Ollama)
- PDF processing limits and thresholds
- Flashcard validations and parameters

## 🔌 API Endpoints

### POST /upload-pdf

**Description**: Processes a PDF file and generates flashcards through AI.

**Parameters**:
- `file`: PDF file (multipart/form-data, max 10MB)

**Response**: JSON event stream (NDJSON)
- Progress events during processing
- Final result with flashcards and statistics

**Events**:
```json
// Progress
{
  "type": "progress",
  "data": {
    "current_part": 1,
    "total_parts": 3,
    "percentage": 33
  }
}

// Completion
{
  "type": "complete",
  "data": {
    "flashcards": [...],
    "statistics": {
      "pages_processed": 10,
      "total_words": 2500,
      "flashcards_generated": 15
    }
  }
}

// Error
{
  "type": "error",
  "data": "Error message"
}
```

### GET /health

**Description**: Checks the status of the application and dependent services.

**Response**:
```json
{
  "status": "healthy",
  "ollama_available": true,
  "model_available": true,
  "models": ["gemma3:4b-it-qat"],
  "error": null
}
```

## 🚦 Error Handling

### Error Types

1. **File Validation Errors** (400):
   - Non-PDF file
   - File too large
   - Insufficient content

2. **AI Service Errors** (500):
   - Ollama unavailable
   - Model not found
   - Generation timeout

3. **Processing Errors** (500):
   - Corrupted or unreadable PDF
   - Content parsing errors

### Logging

All errors are logged with detailed information for debugging:
- INFO level for normal operations
- WARNING level for non-blocking anomalies
- ERROR level for critical errors

## 🔧 Important Configurations

### AI Model
```python
AI_MODEL_NAME = 'gemma3:4b-it-qat'  # Ollama model optimized for Italian
OLLAMA_OPTIONS = {
    "temperature": 0.1,    # Low creativity for consistency
    "num_predict": 1000    # Response token limit
}
```

### Processing Limits
```python
MIN_WORDS_FOR_PROCESSING = 50      # Minimum words for processing
MAX_WORDS_PER_CHUNK = 800          # Maximum words per AI chunk
MAX_FLASHCARDS_LIMIT = 20          # Maximum flashcard limit
```

### Flashcard Validation
```python
VALID_CARD_TYPES = ["multipla", "vero_falso", "aperta"]
MULTIPLE_CHOICE_OPTIONS_COUNT = 4   # Number of multiple choice options
MIN_QUESTION_LENGTH = 5             # Minimum question length
```

## 🏃‍♂️ Startup and Deploy

### Local Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Prerequisites
- Python 3.8+
- Ollama installed and configured
- `gemma3:4b-it-qat` model downloaded

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Test PDF Upload
```bash
curl -X POST -F "file=@test.pdf" http://localhost:8000/upload-pdf
```

## 📊 Monitoring

### Important Metrics
- PDF processing time
- Flashcard generation success rate
- Ollama service availability
- Memory usage during processing

### Key Logs
- `INFO`: Normal operations and milestones
- `WARNING`: Fallbacks and handled anomalies
- `ERROR`: Errors preventing processing 