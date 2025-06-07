# 🔄 REST API Documentation

## 📋 Overview

The backend REST API provides endpoints for PDF document processing and flashcard generation through artificial intelligence. It uses FastAPI for a modern and well-documented interface.

## 🌐 Base URL

```
http://localhost:8000
```

## 📡 Available Endpoints

### POST /upload-pdf

Processes a PDF file and generates flashcards through AI with progress streaming.

#### Request

**Method**: `POST`  
**Content-Type**: `multipart/form-data`  
**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | PDF file to process (max 10MB) |

**cURL Example**:
```bash
curl -X POST \
  http://localhost:8000/upload-pdf \
  -F "file=@document.pdf"
```

#### Response

**Content-Type**: `application/x-ndjson`  
**Format**: Stream of JSON events separated by newlines (NDJSON)

##### Progress Events

```json
{
  "type": "progress",
  "data": {
    "current_part": 2,
    "total_parts": 5,
    "percentage": 40
  }
}
```

**Fields**:
- `current_part`: Part currently being processed (1-based)
- `total_parts`: Total number of parts to process
- `percentage`: Completion percentage (0-100)

##### Completion Event

```json
{
  "type": "complete",
  "data": {
    "flashcards": [
      {
        "domanda": "What is the capital of Italy?",
        "risposta": "Rome",
        "tipo": "aperta",
        "punteggio": 3
      },
      {
        "domanda": "The Earth is flat",
        "risposta": "falso",
        "tipo": "vero_falso",
        "punteggio": 2,
        "giustificazione": "The Earth has a spherical shape..."
      },
      {
        "domanda": "Which of these is a planet?",
        "risposta": "Mars",
        "tipo": "multipla",
        "opzioni": ["Mars", "Moon", "Sun", "Star"],
        "punteggio": 4,
        "giustificazione": "Mars is the only planet among the options..."
      }
    ],
    "statistics": {
      "pages_processed": 10,
      "total_words": 2500,
      "flashcards_generated": 15
    }
  }
}
```

**Flashcard Fields**:
- `domanda`: The question formulated by AI
- `risposta`: The correct answer
- `tipo`: Question type (`aperta`, `vero_falso`, `multipla`)
- `punteggio`: Difficulty from 1 to 5
- `opzioni`: Array of 4 options (only for `multipla` type)
- `giustificazione`: Answer explanation (for `vero_falso` and `multipla` types)

**Statistics Fields**:
- `pages_processed`: Number of pages processed
- `total_words`: Total words extracted
- `flashcards_generated`: Number of flashcards created

##### Error Event

```json
{
  "type": "error",
  "data": "Unable to generate flashcards from PDF content"
}
```

#### Status Codes

| Code | Description | Details |
|------|-------------|---------|
| `200` | Success | NDJSON stream with events |
| `400` | Bad request | Non-PDF file, insufficient content |
| `500` | Server error | AI service unavailable, processing errors |

#### Common Errors

**400 - Invalid file**:
```json
{
  "detail": "File must be a PDF"
}
```

**400 - Insufficient content**:
```json
{
  "detail": "PDF contains too little text to generate meaningful flashcards."
}
```

**500 - AI service unavailable**:
```json
{
  "detail": "AI service unavailable: Connection refused"
}
```

**500 - Model not found**:
```json
{
  "detail": "Required AI model not available"
}
```

---

### GET /health

Checks the health status of the application and dependent services.

#### Request

**Method**: `GET`  
**Parameters**: None

**cURL Example**:
```bash
curl http://localhost:8000/health
```

#### Response

**Content-Type**: `application/json`

##### Success Response

```json
{
  "status": "healthy",
  "ollama_available": true,
  "model_available": true,
  "models": ["gemma3:4b-it-qat", "llama2", "codellama"],
  "error": null
}
```

**Fields**:
- `status`: General status (`healthy` | `unhealthy`)
- `ollama_available`: Ollama is reachable
- `model_available`: Required model is available
- `models`: List of installed models
- `error`: Error message (null if everything is ok)

##### Error Response

```json
{
  "status": "unhealthy",
  "ollama_available": false,
  "model_available": false,
  "models": [],
  "error": "Connection refused"
}
```

#### Status Codes

| Code | Description |
|------|-------------|
| `200` | Always returned (status in body) |

---

## 🔧 Client Configuration

### JavaScript/TypeScript

```typescript
// Base configuration
const API_BASE_URL = 'http://localhost:8000';

// Upload with streaming handling
async function uploadPDF(file: File): Promise<{flashcards: any[], statistics: any}> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload-pdf`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader!.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n').filter(line => line.trim());

    for (const line of lines) {
      const event = JSON.parse(line);
      
      if (event.type === 'progress') {
        console.log(`Progress: ${event.data.percentage}%`);
      } else if (event.type === 'complete') {
        return event.data;
      } else if (event.type === 'error') {
        throw new Error(event.data);
      }
    }
  }
}

// Health check
async function checkHealth(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}
```

### Python

```python
import requests
import json

API_BASE_URL = 'http://localhost:8000'

def upload_pdf(file_path: str):
    """PDF upload and streaming handling"""
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{API_BASE_URL}/upload-pdf',
            files=files,
            stream=True
        )
        
        for line in response.iter_lines():
            if line:
                event = json.loads(line.decode('utf-8'))
                
                if event['type'] == 'progress':
                    print(f"Progress: {event['data']['percentage']}%")
                elif event['type'] == 'complete':
                    return event['data']
                elif event['type'] == 'error':
                    raise Exception(event['data'])

def check_health():
    """Health check"""
    response = requests.get(f'{API_BASE_URL}/health')
    return response.json()
```

## 🚦 Error Handling

### Retry Strategy

For temporary errors (5xx), implement retry with exponential backoff:

```typescript
async function uploadWithRetry(file: File, maxRetries = 3): Promise<any> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await uploadPDF(file);
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      // Exponential backoff: 1s, 2s, 4s
      const delay = Math.pow(2, attempt - 1) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### Timeout

Configure appropriate timeouts for long operations:

```typescript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes

try {
  const response = await fetch(url, {
    signal: controller.signal,
    // ... other options
  });
} finally {
  clearTimeout(timeoutId);
}
```

## 📊 Rate Limiting

Currently not implemented, but production recommendations:

- **Upload**: Max 10 requests/minute per IP
- **Health**: Max 60 requests/minute per IP
- **File size**: Max 10MB per upload

## 🔒 Security

### Implemented Validations

- **File type**: Only PDFs accepted
- **Size**: 10MB limit
- **Content**: Verify presence of extractable text

### Production Recommendations

- Implement authentication (JWT/OAuth)
- Rate limiting to prevent abuse
- Stricter file validation
- Request logging for audit
- Mandatory HTTPS

## 🧪 Testing

### Integration Tests

```bash
# Health check
curl -f http://localhost:8000/health

# Upload test file
curl -X POST \
  -F "file=@test.pdf" \
  http://localhost:8000/upload-pdf \
  --max-time 300
```

### Performance Metrics

- **Small upload** (< 1MB): < 30 seconds
- **Medium upload** (1-5MB): < 2 minutes  
- **Large upload** (5-10MB): < 5 minutes
- **Health check**: < 1 second 