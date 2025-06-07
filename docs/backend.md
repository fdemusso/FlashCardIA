# 🔧 Documentazione Backend

## 📋 Panoramica

Il backend è sviluppato in Python utilizzando FastAPI, fornisce API REST per l'elaborazione di documenti PDF e la generazione di flashcard tramite intelligenza artificiale locale (Ollama).

## 🏗️ Architettura

### Componenti Principali

- **main.py**: Entry point dell'applicazione e routing
- **ai_service.py**: Servizio per la generazione di flashcard tramite IA
- **models.py**: Modelli di dati e strutture
- **validation.py**: Validazione e pulizia delle flashcard generate
- **pdf_processor.py**: Estrazione e elaborazione del testo dai PDF
- **config.py**: Configurazioni e costanti dell'applicazione

## 📄 Documentazione File per File

### 🚀 main.py - Entry Point dell'Applicazione

**Scopo**: Gestisce il routing principale e l'orchestrazione dei servizi.

**Endpoint Principali**:
- `POST /upload-pdf`: Elabora file PDF e genera flashcard
- `GET /health`: Verifica stato dell'applicazione e servizi

**Dipendenze**:
- FastAPI per il framework web
- CORS middleware per la comunicazione con frontend
- StreamingResponse per il progresso in tempo reale

### 🤖 ai_service.py - Servizio Intelligenza Artificiale

**Scopo**: Gestisce l'interazione con Ollama per la generazione di flashcard.

**Funzioni Principali**:
- `generate_flashcards_from_text()`: Genera flashcard da testo usando IA
- `clean_json_response()`: Pulisce e valida le risposte JSON dall'IA
- `check_ollama_availability()`: Verifica disponibilità del servizio Ollama

**Caratteristiche**:
- Prompt engineering ottimizzato per l'italiano
- Gestione robust degli errori di parsing JSON
- Sistema di fallback per risposte malformate

### 📊 models.py - Modelli di Dati

**Scopo**: Definisce le strutture dati utilizzate nell'applicazione.

**Classi**:
- `TextChunk`: Rappresenta una porzione di testo estratto dal PDF
- `FlashcardData`: Struttura per i dati delle flashcard
- `PDFStatistics`: Statistiche di elaborazione del documento
- `ProcessingProgress`: Informazioni sul progresso di elaborazione

### ✅ validation.py - Validazione Flashcard

**Scopo**: Valida e corregge le flashcard generate dall'IA.

**Funzioni**:
- `validate_flashcards()`: Valida una lista di flashcard

**Controlli Effettuati**:
- Verifica campi obbligatori
- Validazione tipi di domande
- Controllo coerenza opzioni multiple choice
- Gestione indici risposta
- Pulizia testi e formattazione

### 📑 pdf_processor.py - Elaborazione PDF

**Scopo**: Estrae e processa il testo dai documenti PDF.

**Funzioni**:
- `extract_text_from_pdf()`: Estrae testo pagina per pagina
- `clean_text()`: Pulisce il testo da caratteri indesiderati
- `merge_chunks_intelligently()`: Raggruppa il testo in porzioni ottimali

**Caratteristiche**:
- Pulizia automatica del testo estratto
- Gestione robusta degli errori di lettura
- Ottimizzazione per l'elaborazione IA

### ⚙️ config.py - Configurazioni

**Scopo**: Centralizza tutte le configurazioni dell'applicazione.

**categorie**:
- Configurazioni CORS e networking
- Parametri per il modello IA (Ollama)
- Limiti e soglie per l'elaborazione PDF
- Validazioni e parametri flashcard

## 🔌 API Endpoints

### POST /upload-pdf

**Descrizione**: Elabora un file PDF e genera flashcard tramite IA.

**Parametri**:
- `file`: File PDF (multipart/form-data, max 10MB)

**Risposta**: Stream di eventi JSON (NDJSON)
- Eventi di progresso durante l'elaborazione
- Risultato finale con flashcard e statistiche

**Eventi**:
```json
// Progresso
{
  "type": "progress",
  "data": {
    "current_part": 1,
    "total_parts": 3,
    "percentage": 33
  }
}

// Completamento
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

// Errore
{
  "type": "error",
  "data": "Messaggio di errore"
}
```

### GET /health

**Descrizione**: Verifica lo stato dell'applicazione e dei servizi dipendenti.

**Risposta**:
```json
{
  "status": "healthy",
  "ollama_available": true,
  "model_available": true,
  "models": ["gemma3:4b-it-qat"],
  "error": null
}
```

## 🚦 Gestione Errori

### Tipologie di Errori

1. **Errori di Validazione File** (400):
   - File non PDF
   - Dimensioni eccessive
   - Contenuto insufficiente

2. **Errori di Servizio IA** (500):
   - Ollama non disponibile
   - Modello non trovato
   - Timeout generazione

3. **Errori di Elaborazione** (500):
   - PDF corrotto o illeggibile
   - Errori parsing contenuto

### Logging

Tutti gli errori sono loggati con informazioni dettagliate per il debugging:
- Livello INFO per operazioni normali
- Livello WARNING per anomalie non bloccanti
- Livello ERROR per errori critici

## 🔧 Configurazioni Importanti

### Modello IA
```python
AI_MODEL_NAME = 'gemma3:4b-it-qat'  # Modello Ollama ottimizzato per italiano
OLLAMA_OPTIONS = {
    "temperature": 0.1,    # Bassa creatività per coerenza
    "num_predict": 1000    # Limite token risposta
}
```

### Limiti di Elaborazione
```python
MIN_WORDS_FOR_PROCESSING = 50      # Minimo parole per elaborazione
MAX_WORDS_PER_CHUNK = 800          # Massimo parole per chunk IA
MAX_FLASHCARDS_LIMIT = 20          # Limite massimo flashcard
```

### Validazione Flashcard
```python
VALID_CARD_TYPES = ["multipla", "vero_falso", "aperta"]
MULTIPLE_CHOICE_OPTIONS_COUNT = 4   # Numero opzioni multiple choice
MIN_QUESTION_LENGTH = 5             # Lunghezza minima domanda
```

## 🏃‍♂️ Avvio e Deploy

### Sviluppo Locale
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Produzione
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Prerequisiti
- Python 3.8+
- Ollama installato e configurato
- Modello `gemma3:4b-it-qat` scaricato

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Test Upload PDF
```bash
curl -X POST -F "file=@test.pdf" http://localhost:8000/upload-pdf
```

## 📊 Monitoring

### Metriche Importanti
- Tempo di elaborazione per PDF
- Successo rate generazione flashcard
- Disponibilità servizio Ollama
- Utilizzo memoria durante elaborazione

### Log Key
- `INFO`: Operazioni normali e milestone
- `WARNING`: Fallback e anomalie gestite
- `ERROR`: Errori che impediscono l'elaborazione 