# 🔄 Documentazione API REST

## 📋 Panoramica

L'API REST del backend fornisce endpoint per l'elaborazione di documenti PDF e la generazione di flashcard tramite intelligenza artificiale. Utilizza FastAPI per un'interfaccia moderna e ben documentata.

## 🌐 Base URL

```
http://localhost:8000
```

## 📡 Endpoint Disponibili

### POST /upload-pdf

Elabora un file PDF e genera flashcard tramite IA con streaming del progresso.

#### Richiesta

**Metodo**: `POST`  
**Content-Type**: `multipart/form-data`  
**Parametri**:

| Parametro | Tipo | Obbligatorio | Descrizione |
|-----------|------|--------------|-------------|
| `file` | File | Sì | File PDF da elaborare (max 10MB) |

**Esempio cURL**:
```bash
curl -X POST \
  http://localhost:8000/upload-pdf \
  -F "file=@documento.pdf"
```

#### Risposta

**Content-Type**: `application/x-ndjson`  
**Formato**: Stream di eventi JSON separati da newline (NDJSON)

##### Eventi di Progresso

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

**Campi**:
- `current_part`: Parte attualmente in elaborazione (1-based)
- `total_parts`: Numero totale di parti da elaborare
- `percentage`: Percentuale di completamento (0-100)

##### Evento di Completamento

```json
{
  "type": "complete",
  "data": {
    "flashcards": [
      {
        "domanda": "Qual è la capitale d'Italia?",
        "risposta": "Roma",
        "tipo": "aperta",
        "punteggio": 3
      },
      {
        "domanda": "La Terra è piatta",
        "risposta": "falso",
        "tipo": "vero_falso",
        "punteggio": 2,
        "giustificazione": "La Terra ha una forma sferica..."
      },
      {
        "domanda": "Quale di questi è un pianeta?",
        "risposta": "Marte",
        "tipo": "multipla",
        "opzioni": ["Marte", "Luna", "Sole", "Stella"],
        "punteggio": 4,
        "giustificazione": "Marte è l'unico pianeta tra le opzioni..."
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

**Campi Flashcard**:
- `domanda`: La domanda formulata dall'IA
- `risposta`: La risposta corretta
- `tipo`: Tipo di domanda (`aperta`, `vero_falso`, `multipla`)
- `punteggio`: Difficoltà da 1 a 5
- `opzioni`: Array di 4 opzioni (solo per tipo `multipla`)
- `giustificazione`: Spiegazione della risposta (per tipi `vero_falso` e `multipla`)

**Campi Statistics**:
- `pages_processed`: Numero di pagine elaborate
- `total_words`: Parole totali estratte
- `flashcards_generated`: Numero di flashcard create

##### Evento di Errore

```json
{
  "type": "error",
  "data": "Impossibile generare flashcard dal contenuto del PDF"
}
```

#### Codici di Stato

| Codice | Descrizione | Dettagli |
|--------|-------------|----------|
| `200` | Successo | Stream NDJSON con eventi |
| `400` | Richiesta non valida | File non PDF, contenuto insufficiente |
| `500` | Errore server | Servizio IA non disponibile, errori elaborazione |

#### Errori Comuni

**400 - File non valido**:
```json
{
  "detail": "Il file deve essere un PDF"
}
```

**400 - Contenuto insufficiente**:
```json
{
  "detail": "Il PDF contiene troppo poco testo per generare flashcard significative."
}
```

**500 - Servizio IA non disponibile**:
```json
{
  "detail": "Servizio IA non disponibile: Connection refused"
}
```

**500 - Modello non trovato**:
```json
{
  "detail": "Modello IA richiesto non disponibile"
}
```

---

### GET /health

Verifica lo stato di salute dell'applicazione e dei servizi dipendenti.

#### Richiesta

**Metodo**: `GET`  
**Parametri**: Nessuno

**Esempio cURL**:
```bash
curl http://localhost:8000/health
```

#### Risposta

**Content-Type**: `application/json`

##### Risposta di Successo

```json
{
  "status": "healthy",
  "ollama_available": true,
  "model_available": true,
  "models": ["gemma3:4b-it-qat", "llama2", "codellama"],
  "error": null
}
```

**Campi**:
- `status`: Stato generale (`healthy` | `unhealthy`)
- `ollama_available`: Ollama è raggiungibile
- `model_available`: Il modello richiesto è disponibile
- `models`: Lista dei modelli installati
- `error`: Messaggio di errore (null se tutto ok)

##### Risposta di Errore

```json
{
  "status": "unhealthy",
  "ollama_available": false,
  "model_available": false,
  "models": [],
  "error": "Connection refused"
}
```

#### Codici di Stato

| Codice | Descrizione |
|--------|-------------|
| `200` | Sempre restituito (stato nel body) |

---

## 🔧 Configurazione Client

### JavaScript/TypeScript

```typescript
// Configurazione base
const API_BASE_URL = 'http://localhost:8000';

// Upload con gestione streaming
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
        console.log(`Progresso: ${event.data.percentage}%`);
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
    """Upload PDF e gestione streaming"""
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
                    print(f"Progresso: {event['data']['percentage']}%")
                elif event['type'] == 'complete':
                    return event['data']
                elif event['type'] == 'error':
                    raise Exception(event['data'])

def check_health():
    """Health check"""
    response = requests.get(f'{API_BASE_URL}/health')
    return response.json()
```

## 🚦 Gestione Errori

### Strategia di Retry

Per errori temporanei (5xx), implementare retry con backoff esponenziale:

```typescript
async function uploadWithRetry(file: File, maxRetries = 3): Promise<any> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await uploadPDF(file);
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      // Backoff esponenziale: 1s, 2s, 4s
      const delay = Math.pow(2, attempt - 1) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### Timeout

Configurare timeout appropriati per operazioni lunghe:

```typescript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minuti

try {
  const response = await fetch(url, {
    signal: controller.signal,
    // ... altre opzioni
  });
} finally {
  clearTimeout(timeoutId);
}
```

## 📊 Rate Limiting

Attualmente non implementato, ma raccomandazioni per produzione:

- **Upload**: Max 10 richieste/minuto per IP
- **Health**: Max 60 richieste/minuto per IP
- **File size**: Max 10MB per upload

## 🔒 Sicurezza

### Validazioni Implementate

- **Tipo file**: Solo PDF accettati
- **Dimensione**: Limite 10MB
- **Contenuto**: Verifica presenza testo estraibile

### Raccomandazioni Produzione

- Implementare autenticazione (JWT/OAuth)
- Rate limiting per prevenire abuse
- Validazione più rigorosa dei file
- Logging delle richieste per audit
- HTTPS obbligatorio

## 🧪 Testing

### Test di Integrazione

```bash
# Health check
curl -f http://localhost:8000/health

# Upload test file
curl -X POST \
  -F "file=@test.pdf" \
  http://localhost:8000/upload-pdf \
  --max-time 300
```

### Metriche di Performance

- **Upload piccolo** (< 1MB): < 30 secondi
- **Upload medio** (1-5MB): < 2 minuti  
- **Upload grande** (5-10MB): < 5 minuti
- **Health check**: < 1 secondo 