# 🎯 Generatore di Flashcard IA

Un'applicazione web moderna che genera flashcard educative personalizzate da documenti PDF utilizzando l'intelligenza artificiale locale (Ollama con modello Gemma). Il sistema è stato progettato con architettura modulare sia nel backend che nel frontend per garantire scalabilità e manutenibilità.

## ✨ Caratteristiche Principali

### 🤖 Generazione IA Avanzata
- **3 tipi di domande**: Multiple choice, Vero/Falso, Domande aperte
- **Giustificazioni automatiche**: Spiegazioni dettagliate per ogni risposta
- **Validazione intelligente**: Sistema di fallback per garantire coerenza delle risposte
- **Punteggio di difficoltà**: Ogni flashcard ha un livello di difficoltà da 1 a 5

### 🏗️ Architettura Modulare
- **Backend modularizzato**: Separazione in servizi (`ai_service`, `models`, `validation`)
- **Frontend con hook personalizzati**: Logica business separata dalla UI
- **Componenti riutilizzabili**: Architettura scalabile e manutenibile
- **Type Safety completo**: TypeScript per ridurre errori runtime

### 🎨 Interfaccia Utente Moderna
- **Design responsive**: Ottimizzato per ogni dispositivo
- **Progress tracking**: Barra di progresso durante l'elaborazione
- **Feedback visivo**: Indicatori chiari per risposte corrette/errate
- **Navigazione intuitiva**: Controlli semplici e accessibili

## 📋 Requisiti di Sistema

### Software Necessario
- **Python** 3.8 o superiore
- **Node.js** 16 o superiore  
- **Ollama** (versione più recente)
- **Git** (per il clone del repository)

### Modello IA
Il progetto utilizza il modello `gemma3:4b-it-qat` di Ollama, ottimizzato per l'italiano.

## 🚀 Installazione Rapida

### 1. Setup Ollama
```bash
# Installa Ollama da https://ollama.ai/
# Poi scarica il modello:
ollama pull gemma3:4b-it-qat
```

### 2. Clone e Setup Backend
```bash
git clone <repository-url>
cd IA-flashcard

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia backend
cd backend
uvicorn main:app --reload
```

### 3. Setup Frontend
```bash
# In una nuova finestra terminale
cd frontend
npm install
npm start
```

## 🎮 Come Utilizzare

1. **Verifica prerequisiti**: Assicurati che Ollama sia attivo con il modello corretto
2. **Accedi all'app**: Apri `http://localhost:3000` nel browser
3. **Carica PDF**: Seleziona un documento PDF (max 10MB)
4. **Attendi elaborazione**: Il sistema processa il documento e genera le flashcard
5. **Studia**: Naviga tra le flashcard e verifica le tue conoscenze

## 🏛️ Architettura del Progetto

### Backend (Python + FastAPI)
```
backend/
├── main.py              # Entry point e routing
├── ai_service.py        # Logica generazione IA
├── models.py            # Modelli dati Pydantic  
├── validation.py        # Validazione risposte
└── pdf_processor.py     # Elaborazione PDF
```

### Frontend (React + TypeScript)
```
frontend/src/
├── components/
│   ├── FlashcardViewer/    # Visualizzazione flashcard
│   ├── FileUpload/         # Gestione upload
│   ├── Statistics/         # Statistiche documento
│   └── common/             # Componenti condivisi
├── hooks/                  # Custom hooks business logic
├── services/               # API e servizi esterni
├── types/                  # Interfacce TypeScript
└── App.tsx                # Orchestratore principale
```

## 🧪 Testing e Verifica

### Health Check
```bash
curl http://localhost:8000/health
```

### Test Componenti
```bash
# Backend
cd backend
python -m pytest

# Frontend  
cd frontend
npm test
```

## 🔧 Risoluzione Problemi

### Problemi Comuni

| Problema | Soluzione |
|----------|-----------|
| **Ollama non risponde** | Verifica che il servizio sia attivo: `ollama list` |
| **Modello non trovato** | Scarica il modello: `ollama pull gemma3:4b-it-qat` |
| **Errori CORS** | Assicurati che frontend sia su porta 3000 |
| **PDF troppo grande** | Limite 10MB, riduci dimensioni file |
| **Timeout elaborazione** | File complessi richiedono più tempo |

### Log e Debug
- **Backend logs**: Console dove gira `uvicorn`
- **Frontend logs**: DevTools del browser (F12)
- **Ollama logs**: `ollama logs`

## 📈 Roadmap e Contributi

### Prossime Funzionalità
- [ ] Esportazione flashcard in formati esterni
- [ ] Sistema di revisione spaziale
- [ ] Supporto per più modelli IA
- [ ] Modalità offline completa
- [ ] Analytics di apprendimento

### Come Contribuire
1. **Fork** del repository
2. **Crea branch** per la feature: `git checkout -b feature/nome-feature`
3. **Commit** modifiche: `git commit -m 'Aggiungi nuova feature'`
4. **Push** al branch: `git push origin feature/nome-feature`
5. **Apri Pull Request**

## 📊 Versioning

Vedi [CHANGELOG.md](CHANGELOG.md) per la cronologia dettagliata delle versioni.

- **v3.0**: Refactoring completo frontend con architettura modulare
- **v2.1**: Correzione coerenza risposte multiple choice
- **v2.0**: Aggiunta giustificazioni automatiche
- **v1.0**: Release iniziale

## 📝 Licenza

Questo progetto è rilasciato sotto **licenza MIT**. Vedi [LICENSE](LICENSE) per i dettagli.

---

⭐ **Se questo progetto ti è utile, lascia una stella su GitHub!** 