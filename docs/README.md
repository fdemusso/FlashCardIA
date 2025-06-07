# 📚 Documentazione Completa - Generatore di Flashcard IA

## 🏗️ Panoramica dell'Architettura

Questo progetto è diviso in due parti principali:
- **Backend**: API REST in Python con FastAPI che gestisce l'elaborazione PDF e la generazione di flashcard tramite IA
- **Frontend**: Applicazione React+TypeScript per l'interfaccia utente

## 📂 Struttura del Progetto

```
IA-flashcard/
├── backend/               # API FastAPI in Python
│   ├── main.py           # Entry point e routing principale
│   ├── ai_service.py     # Servizio per generazione flashcard con Ollama
│   ├── models.py         # Modelli di dati Pydantic/DataClass
│   ├── validation.py     # Validazione e pulizia flashcard
│   ├── pdf_processor.py  # Estrazione e elaborazione testo PDF
│   └── config.py         # Configurazioni e costanti
├── frontend/             # Applicazione React
│   └── src/
│       ├── App.tsx       # Componente principale
│       ├── components/   # Componenti React riutilizzabili
│       ├── hooks/        # Custom hooks per logica business
│       ├── services/     # Servizi API e comunicazione
│       ├── types/        # Definizioni TypeScript
│       └── utils/        # Utility e helper functions
└── docs/                 # Documentazione completa
```

## 🔄 Flusso di Funzionamento

1. **Upload PDF**: L'utente carica un file PDF tramite l'interfaccia
2. **Estrazione Testo**: Il backend estrae e pulisce il testo dal PDF
3. **Generazione IA**: Il testo viene inviato a Ollama per generare flashcard
4. **Validazione**: Le flashcard vengono validate e corrette
5. **Visualizzazione**: Il frontend presenta le flashcard in modo interattivo

## 📖 Sezioni della Documentazione

- [📱 **Frontend**](./frontend.md) - Documentazione completa dei componenti React
- [🔧 **Backend**](./backend.md) - Documentazione dell'API e servizi Python
- [🚀 **Deploy**](./deployment.md) - Guida al deployment e configurazione
- [🧪 **Testing**](./testing.md) - Guide per test e debugging
- [🔄 **API**](./api.md) - Documentazione delle API REST

## 🛠️ Tecnologie Utilizzate

### Backend
- **FastAPI**: Framework web moderno per Python
- **Ollama**: Servizio IA locale per generazione testo
- **PyPDF2**: Libreria per estrazione testo da PDF
- **Pydantic**: Validazione dati e serializzazione

### Frontend
- **React**: Libreria UI per JavaScript
- **TypeScript**: Superset tipizzato di JavaScript
- **Tailwind CSS**: Framework CSS utility-first
- **Custom Hooks**: Pattern per logica business riutilizzabile

## 🎯 Funzionalità Principali

### 🤖 Generazione IA Intelligente
- **3 Tipi di Domande**: Multiple choice, Vero/Falso, Aperte
- **Giustificazioni Automatiche**: Spiegazioni per ogni risposta
- **Validazione Robusta**: Sistema di fallback per coerenza
- **Punteggio Difficoltà**: Rating da 1 a 5 per ogni flashcard

### 🎨 Interfaccia Moderna
- **Design Responsive**: Funziona su ogni dispositivo
- **Progress Tracking**: Barra di progresso real-time
- **Feedback Visivo**: Indicatori per risposte corrette/errate
- **Navigazione Fluida**: Controlli intuitivi

### 🔧 Architettura Modulare
- **Separazione Concern**: Backend e frontend ben separati
- **Hook Personalizzati**: Logica business isolata
- **Componenti Riutilizzabili**: Codice DRY e manutenibile
- **Type Safety**: TypeScript per ridurre errori

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

## 📞 Supporto

Per domande specifiche, consulta le sezioni dedicate della documentazione o apri un issue su GitHub. 