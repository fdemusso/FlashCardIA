# Generatore di Flashcard IA

Un'applicazione web che genera flashcard educative da documenti PDF utilizzando l'IA locale (Ollama con modello Gemma).

## Requisiti di Sistema

### Software Necessario
- Python 3.8 o superiore
- Node.js 14 o superiore
- Ollama (versione più recente)
- Git (opzionale, per il clone del repository)

### Modello IA
Il progetto utilizza il modello `gemma3:4b-it-qat` di Ollama. Questo modello è ottimizzato per l'italiano e deve essere scaricato prima di utilizzare l'applicazione.

## Installazione

### 1. Installazione di Ollama

1. Scarica Ollama dal sito ufficiale: https://ollama.ai/
2. Installa Ollama seguendo le istruzioni per il tuo sistema operativo
3. Scarica il modello necessario:
```bash
ollama pull gemma3:4b-it-qat
```

### 2. Backend

1. Crea un ambiente virtuale Python:
```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Avvia il server backend:
```bash
cd backend
uvicorn main:app --reload
```

### 3. Frontend

1. Installa le dipendenze:
```bash
cd frontend
npm install
```

2. Avvia il server di sviluppo:
```bash
npm start
```

## Utilizzo

1. Assicurati che Ollama sia in esecuzione con il modello corretto
2. Apri il browser e vai a `http://localhost:3000`
3. Carica un file PDF
4. Attendi la generazione delle flashcard
5. Naviga tra le flashcard utilizzando i pulsanti "Precedente" e "Successiva"
6. Rispondi alle domande e verifica le tue risposte

## Caratteristiche

- Generazione di flashcard da PDF
- Tre tipi di domande:
  - Domande a scelta multipla
  - Vero/Falso
  - Domande aperte
- Sistema di punteggio per ogni flashcard
- Interfaccia responsive ottimizzata per MacBook Air 15"
- Integrazione con Ollama per l'elaborazione locale
- Supporto multilingua (ottimizzato per l'italiano)

## Risoluzione dei Problemi

### Verifica dell'Installazione
Per verificare che tutto sia configurato correttamente, puoi utilizzare l'endpoint di health check:
```bash
curl http://localhost:8000/health
```

### Problemi Comuni
1. **Ollama non risponde**: Assicurati che il servizio Ollama sia in esecuzione
2. **Modello non trovato**: Verifica di aver scaricato il modello corretto con `ollama list`
3. **Errori di CORS**: Verifica che il frontend stia girando sulla porta corretta (3000)

## Contribuire

Se desideri contribuire al progetto:
1. Fai un fork del repository
2. Crea un branch per la tua feature
3. Invia una pull request

## Licenza

Questo progetto è rilasciato sotto licenza MIT. 