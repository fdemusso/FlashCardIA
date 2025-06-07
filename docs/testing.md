# 🧪 Testing and Debugging Guide

## 📋 Overview

This guide provides comprehensive strategies for testing and debugging the AI Flashcard Generator application, covering both the Python backend and React frontend.

## 🏗️ Testing Strategy

### Test Pyramid

```
    🔺 E2E Tests
   🔺🔺 Integration Tests  
  🔺🔺🔺 Unit Tests
```

- **Unit Tests**: Individual functions and isolated components
- **Integration Tests**: Interaction between modules
- **E2E Tests**: Complete user flows

### Target Coverage

- **Backend**: 80%+ code coverage
- **Frontend**: 70%+ component coverage
- **API**: 100% endpoints tested
- **Critical Path**: 95%+ coverage

## 🔧 Backend Testing

### Test Environment Setup

```bash
# Install test dependencies
cd backend
pip install pytest pytest-cov pytest-asyncio httpx

# Test structure
mkdir -p tests/{unit,integration,fixtures}
touch tests/__init__.py
```

### pytest Configuration

```python
# backend/pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -v
```

### Unit Tests

#### Test AI Service

```python
# tests/unit/test_ai_service.py
import pytest
from unittest.mock import Mock, patch
from ai_service import generate_flashcards_from_text, clean_json_response

class TestAIService:
    
    def test_clean_json_response_valid_array(self):
        """Test valid JSON response cleanup"""
        input_text = '```json\n[{"domanda": "test"}]\n```'
        result = clean_json_response(input_text)
        assert result == '[{"domanda": "test"}]'
    
    def test_clean_json_response_single_object(self):
        """Test single object to array conversion"""
        input_text = '{"domanda": "test"}'
        result = clean_json_response(input_text)
        assert result == '[{"domanda": "test"}]'
    
    def test_clean_json_response_empty(self):
        """Test empty input handling"""
        result = clean_json_response("")
        assert result == "[]"
    
    @patch('ai_service.ollama.generate')
    def test_generate_flashcards_success(self, mock_generate):
        """Test successful flashcard generation"""
        # Mock Ollama response
        mock_generate.return_value = {
            'response': '[{"domanda": "Test?", "risposta": "Answer", "tipo": "aperta", "punteggio": 3}]'
        }
        
        result = generate_flashcards_from_text("Test text")
        
        assert len(result) == 1
        assert result[0]['domanda'] == "Test?"
        assert result[0]['tipo'] == "aperta"
    
    @patch('ai_service.ollama.generate')
    def test_generate_flashcards_ollama_error(self, mock_generate):
        """Test Ollama error handling"""
        mock_generate.side_effect = Exception("Connection error")
        
        result = generate_flashcards_from_text("Test text")
        
        assert result == []
```

#### Test PDF Processor

```python
# tests/unit/test_pdf_processor.py
import pytest
from io import BytesIO
from unittest.mock import Mock, patch
from pdf_processor import clean_text, merge_chunks_intelligently
from models import TextChunk

class TestPDFProcessor:
    
    def test_clean_text_removes_control_chars(self):
        """Test rimozione caratteri di controllo"""
        dirty_text = "Testo\x00con\x1fcaratteri\x7fdi controllo"
        clean = clean_text(dirty_text)
        assert "\x00" not in clean
        assert "\x1f" not in clean
        assert "\x7f" not in clean
    
    def test_clean_text_normalizes_spaces(self):
        """Test normalizzazione spazi"""
        text_with_spaces = "Testo   con    spazi     multipli"
        clean = clean_text(text_with_spaces)
        assert "   " not in clean
        assert clean == "Testo con spazi multipli"
    
    def test_clean_text_removes_short_lines(self):
        """Test rimozione linee troppo corte"""
        text_with_short_lines = "Linea normale\nab\nAltra linea normale\nx"
        clean = clean_text(text_with_short_lines)
        assert "ab" not in clean
        assert "x" not in clean
        assert "Linea normale" in clean
    
    def test_merge_chunks_respects_limit(self):
        """Test rispetto limite parole nel merge"""
        chunks = [
            TextChunk("Primo chunk con molte parole", 1, 5),
            TextChunk("Secondo chunk", 2, 2),
            TextChunk("Terzo chunk", 3, 2)
        ]
        
        merged = merge_chunks_intelligently(chunks, max_words=6)
        
        assert len(merged) == 2  # Primo chunk + secondo, poi terzo
        assert "Primo chunk" in merged[0]
        assert "Secondo chunk" in merged[0]
        assert "Terzo chunk" in merged[1]
```

#### Test Validation

```python
# tests/unit/test_validation.py
import pytest
from validation import validate_flashcards

class TestValidation:
    
    def test_validate_flashcards_valid_input(self):
        """Test validazione input valido"""
        flashcards = [{
            "domanda": "Domanda test",
            "risposta": "Risposta test",
            "tipo": "aperta",
            "punteggio": 3
        }]
        
        result = validate_flashcards(flashcards)
        
        assert len(result) == 1
        assert result[0]["domanda"] == "Domanda test"
    
    def test_validate_flashcards_missing_fields(self):
        """Test gestione campi mancanti"""
        flashcards = [{"domanda": "Solo domanda"}]
        
        result = validate_flashcards(flashcards)
        
        assert len(result) == 0  # Scartata per campi mancanti
    
    def test_validate_multiple_choice_conversion(self):
        """Test conversione indice risposta multiple choice"""
        flashcards = [{
            "domanda": "Test multiple choice",
            "risposta": 1,  # Indice
            "tipo": "multipla",
            "opzioni": ["A", "B", "C", "D"],
            "punteggio": 3,
            "giustificazione": "Test"
        }]
        
        result = validate_flashcards(flashcards)
        
        assert result[0]["risposta"] == "B"  # Convertito da indice a testo
```

### Integration Tests

```python
# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAPIEndpoints:
    
    def test_health_endpoint(self):
        """Test endpoint health"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "ollama_available" in data
    
    @pytest.mark.asyncio
    async def test_upload_pdf_invalid_file(self):
        """Test upload file non PDF"""
        # File di test non PDF
        fake_file = BytesIO(b"Not a PDF content")
        
        response = client.post(
            "/upload-pdf",
            files={"file": ("test.txt", fake_file, "text/plain")}
        )
        
        assert response.status_code == 400
        assert "deve essere un PDF" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_upload_pdf_empty_file(self):
        """Test upload file vuoto"""
        empty_file = BytesIO(b"")
        
        response = client.post(
            "/upload-pdf",
            files={"file": ("empty.pdf", empty_file, "application/pdf")}
        )
        
        assert response.status_code == 400
```

### Test con Mock Ollama

```python
# tests/fixtures/ollama_mock.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_ollama_success():
    """Mock Ollama con risposta di successo"""
    mock = Mock()
    mock.generate.return_value = {
        'response': '''[
            {
                "domanda": "Test domanda",
                "risposta": "Test risposta", 
                "tipo": "aperta",
                "punteggio": 3
            }
        ]'''
    }
    mock.list.return_value = {
        'models': [{'name': 'gemma3:4b-it-qat'}]
    }
    return mock

@pytest.fixture
def mock_ollama_error():
    """Mock Ollama con errore"""
    mock = Mock()
    mock.generate.side_effect = Exception("Connection refused")
    mock.list.side_effect = Exception("Service unavailable")
    return mock
```

### Comandi Test Backend

```bash
# Esecuzione tutti i test
pytest

# Test con copertura
pytest --cov=. --cov-report=html

# Test specifici
pytest tests/unit/test_ai_service.py

# Test con output verboso
pytest -v -s

# Test paralleli
pytest -n auto

# Test solo falliti
pytest --lf
```

## 📱 Testing Frontend

### Setup Ambiente Test

```bash
cd frontend

# Dipendenze già incluse in create-react-app
# Testing Library, Jest sono preconfigurati

# Installazione aggiuntive per test avanzati
npm install --save-dev @testing-library/user-event msw
```

### Configurazione Test

```javascript
// frontend/src/setupTests.js
import '@testing-library/jest-dom';
import { server } from './mocks/server';

// Setup MSW
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Mock Service Worker (MSW)

```javascript
// frontend/src/mocks/handlers.js
import { rest } from 'msw';

export const handlers = [
  // Mock health endpoint
  rest.get('http://localhost:8000/health', (req, res, ctx) => {
    return res(
      ctx.json({
        status: 'healthy',
        ollama_available: true,
        model_available: true
      })
    );
  }),

  // Mock upload endpoint
  rest.post('http://localhost:8000/upload-pdf', (req, res, ctx) => {
    return res(
      ctx.text(`{"type":"progress","data":{"percentage":50}}
{"type":"complete","data":{"flashcards":[],"statistics":{}}}`)
    );
  })
];

// frontend/src/mocks/server.js
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Unit Tests Componenti

```javascript
// frontend/src/components/FileUpload/FileUpload.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FileUpload } from './FileUpload';

describe('FileUpload Component', () => {
  const mockProps = {
    uploadState: {
      file: null,
      loading: false,
      error: null,
      loadingMessage: '',
      generationProgress: null
    },
    onFileChange: jest.fn(),
    onUpload: jest.fn(),
    onErrorDismiss: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders upload interface', () => {
    render(<FileUpload {...mockProps} />);
    
    expect(screen.getByText(/carica un file pdf/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /seleziona file/i })).toBeInTheDocument();
  });

  test('handles file selection', async () => {
    const user = userEvent.setup();
    render(<FileUpload {...mockProps} />);
    
    const file = new File(['pdf content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/seleziona file/i);
    
    await user.upload(input, file);
    
    expect(mockProps.onFileChange).toHaveBeenCalledWith(file);
  });

  test('shows loading state', () => {
    const loadingProps = {
      ...mockProps,
      uploadState: { ...mockProps.uploadState, loading: true, loadingMessage: 'Elaborazione...' }
    };
    
    render(<FileUpload {...loadingProps} />);
    
    expect(screen.getByText('Elaborazione...')).toBeInTheDocument();
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  test('shows error message', () => {
    const errorProps = {
      ...mockProps,
      uploadState: { ...mockProps.uploadState, error: 'Errore di upload' }
    };
    
    render(<FileUpload {...errorProps} />);
    
    expect(screen.getByText('Errore di upload')).toBeInTheDocument();
  });
});
```

### Test Custom Hooks

```javascript
// frontend/src/hooks/useFileUpload.test.ts
import { renderHook, act } from '@testing-library/react';
import { useFileUpload } from './useFileUpload';

describe('useFileUpload Hook', () => {
  test('initial state', () => {
    const { result } = renderHook(() => useFileUpload());
    
    expect(result.current.uploadState.file).toBeNull();
    expect(result.current.uploadState.loading).toBe(false);
    expect(result.current.uploadState.error).toBeNull();
  });

  test('setFile updates state', () => {
    const { result } = renderHook(() => useFileUpload());
    const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });
    
    act(() => {
      result.current.setFile(file);
    });
    
    expect(result.current.uploadState.file).toBe(file);
  });

  test('uploadFile handles success', async () => {
    const { result } = renderHook(() => useFileUpload());
    const file = new File(['content'], 'test.pdf', { type: 'application/pdf' });
    
    act(() => {
      result.current.setFile(file);
    });

    await act(async () => {
      const response = await result.current.uploadFile();
      expect(response).toBeDefined();
    });
  });
});
```

### Integration Tests

```javascript
// frontend/src/App.test.tsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

describe('App Integration', () => {
  test('complete upload flow', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Verifica stato iniziale
    expect(screen.getByText(/generatore di flashcard ia/i)).toBeInTheDocument();
    expect(screen.getByText(/carica un file pdf/i)).toBeInTheDocument();
    
    // Simula selezione file
    const file = new File(['pdf content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/seleziona file/i);
    await user.upload(input, file);
    
    // Simula upload
    const uploadButton = screen.getByRole('button', { name: /genera flashcard/i });
    await user.click(uploadButton);
    
    // Verifica transizione a modalità flashcard
    await waitFor(() => {
      expect(screen.queryByText(/carica un file pdf/i)).not.toBeInTheDocument();
    });
  });
});
```

### Comandi Test Frontend

```bash
# Esecuzione test
npm test

# Test con copertura
npm test -- --coverage

# Test in modalità watch
npm test -- --watch

# Test specifici
npm test -- FileUpload.test.tsx

# Test senza watch (CI)
npm test -- --watchAll=false
```

## 🔍 Debugging

### Backend Debugging

#### Setup VSCode

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI Debug",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/main.py",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      },
      "args": []
    }
  ]
}
```

#### Logging Avanzato

```python
# backend/debug_config.py
import logging
import sys

def setup_debug_logging():
    """Configurazione logging per debugging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Logger specifici
    logging.getLogger('ai_service').setLevel(logging.DEBUG)
    logging.getLogger('pdf_processor').setLevel(logging.DEBUG)
    logging.getLogger('validation').setLevel(logging.DEBUG)
```

#### Profiling Performance

```python
# backend/profiling.py
import cProfile
import pstats
from functools import wraps

def profile_function(func):
    """Decorator per profiling funzioni"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 funzioni
        
        return result
    return wrapper

# Uso
@profile_function
def generate_flashcards_from_text(text):
    # ... implementazione
    pass
```

### Frontend Debugging

#### React DevTools

```javascript
// Installazione React DevTools browser extension
// Debugging componenti e stato in tempo reale
```

#### Debug Custom Hooks

```javascript
// frontend/src/hooks/useDebug.ts
import { useEffect, useRef } from 'react';

export function useDebug(value: any, name: string) {
  const prevValue = useRef(value);
  
  useEffect(() => {
    if (prevValue.current !== value) {
      console.log(`[${name}] changed:`, {
        from: prevValue.current,
        to: value
      });
      prevValue.current = value;
    }
  });
}

// Uso nei componenti
function MyComponent() {
  const [state, setState] = useState(initialState);
  useDebug(state, 'MyComponent.state');
  
  // ...
}
```

#### Network Debugging

```javascript
// frontend/src/utils/apiDebug.ts
const originalFetch = window.fetch;

window.fetch = function(...args) {
  console.log('API Request:', args);
  
  return originalFetch.apply(this, args)
    .then(response => {
      console.log('API Response:', response);
      return response;
    })
    .catch(error => {
      console.error('API Error:', error);
      throw error;
    });
};
```

## 🚨 Troubleshooting Comune

### Backend Issues

#### Ollama Connection

```bash
# Verifica servizio Ollama
curl http://localhost:11434/api/tags

# Debug connessione
python -c "import ollama; print(ollama.list())"

# Logs Ollama
journalctl -u ollama -f
```

#### Memory Issues

```python
# Monitoring memoria
import psutil
import gc

def check_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    print(f"RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
    
    # Garbage collection
    collected = gc.collect()
    print(f"Garbage collected: {collected} objects")
```

### Frontend Issues

#### Bundle Analysis

```bash
# Analisi bundle size
npm install --save-dev webpack-bundle-analyzer
npm run build
npx webpack-bundle-analyzer build/static/js/*.js
```

#### Performance Debugging

```javascript
// Performance monitoring
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  console.log(metric);
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

## 📊 Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage --watchAll=false
```

### Quality Gates

```yaml
# Soglie qualità
coverage:
  range: 80..100
  round: down
  precision: 2

status:
  project:
    default:
      target: 80%
  patch:
    default:
      target: 70%
```

Questa documentazione fornisce una guida completa per testare e debuggare l'applicazione, con esempi pratici e strategie per mantenere alta la qualità del codice. 