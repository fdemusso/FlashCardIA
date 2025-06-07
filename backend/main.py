"""
Modulo principale dell'applicazione FastAPI per la generazione di flashcard da PDF.

Questo modulo gestisce:
- Il routing principale dell'API REST
- L'elaborazione di file PDF caricati dall'utente
- L'orchestrazione dei servizi per la generazione di flashcard
- La gestione delle risposte streaming per il progresso in tempo reale
- La configurazione CORS per la comunicazione con il frontend

Endpoint principali:
- POST /upload-pdf: Elabora PDF e genera flashcard tramite IA
- GET /health: Verifica stato dell'applicazione e servizi dipendenti
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
import json
import logging
import asyncio

# Import dei moduli personalizzati
from config import ALLOWED_ORIGINS, MIN_WORDS_FOR_PROCESSING, MAX_FLASHCARDS_LIMIT
from models import TextChunk, PDFStatistics, ProcessingProgress
from pdf_processor import extract_text_from_pdf, merge_chunks_intelligently
from ai_service import generate_flashcards_from_text, check_ollama_availability

# Configurazione del logger per tracciare le operazioni
logger = logging.getLogger(__name__)

# Inizializzazione dell'applicazione FastAPI
app = FastAPI()

# Configurazione CORS per permettere le richieste dal frontend React
# Permette tutte le origini specificate in config.py durante lo sviluppo
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Domini autorizzati (localhost:3000, etc.)
    allow_credentials=True,         # Permette l'invio di cookie e credenziali
    allow_methods=["*"],           # Permette tutti i metodi HTTP
    allow_headers=["*"],           # Permette tutti gli header
)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Endpoint principale per l'elaborazione di file PDF e la generazione di flashcard.
    
    Questo endpoint:
    1. Valida il file PDF ricevuto
    2. Estrae il testo dal PDF pagina per pagina
    3. Verifica la disponibilità del servizio IA (Ollama)
    4. Genera flashcard tramite IA in modo progressivo
    5. Restituisce un stream di eventi con progresso e risultati
    
    Args:
        file (UploadFile): File PDF caricato dall'utente (max 10MB)
    
    Returns:
        StreamingResponse: Stream NDJSON con eventi di progresso e risultato finale
        
    Raises:
        HTTPException: 
            - 400: File non valido, contenuto insufficiente
            - 500: Servizio IA non disponibile, errori di elaborazione
    """
    try:
        # Validazione: verifica che il file sia effettivamente un PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Il file deve essere un PDF")
        
        # Lettura del contenuto del file PDF in memoria
        content = await file.read()
        pdf_file = io.BytesIO(content)
        
        # Fase 1: Estrazione del testo dal PDF
        logger.info("Inizio estrazione testo dal PDF...")
        chunks = extract_text_from_pdf(pdf_file)
        
        # Verifica che sia stato estratto del testo valido
        if not chunks:
            raise HTTPException(status_code=400, detail="Impossibile estrarre testo dal PDF. Il file potrebbe essere un'immagine o essere danneggiato.")
        
        # Calcolo delle statistiche del documento elaborato
        total_words = sum(chunk.word_count for chunk in chunks)
        logger.info(f"Estratto testo da {len(chunks)} pagine, totale {total_words} parole")
        
        # Verifica che ci sia abbastanza contenuto per generare flashcard significative
        if total_words < MIN_WORDS_FOR_PROCESSING:
            raise HTTPException(status_code=400, detail="Il PDF contiene troppo poco testo per generare flashcard significative.")
        
        # Fase 2: Raggruppamento intelligente del testo in porzioni ottimali per l'IA
        merged_texts = merge_chunks_intelligently(chunks)
        
        # Fase 3: Verifica della disponibilità del servizio IA (Ollama)
        logger.info("Verifica disponibilità Ollama...")
        ollama_status = check_ollama_availability()
        
        # Controllo se Ollama è disponibile e funzionante
        if not ollama_status["available"]:
            raise HTTPException(status_code=500, detail=f"Servizio IA non disponibile: {ollama_status.get('error', 'Errore sconosciuto')}")
        
        # Controllo se il modello richiesto è disponibile
        if not ollama_status["model_available"]:
            raise HTTPException(status_code=500, detail="Modello IA richiesto non disponibile")
        
        logger.info("Modello IA disponibile")

        async def generate():
            """
            Funzione generatore asincrona per l'elaborazione streaming.
            
            Genera flashcard per ogni porzione di testo e invia eventi di progresso
            in tempo reale al client. Utilizza il formato NDJSON per trasmettere
            multiple righe JSON separate.
            
            Yields:
                str: Eventi JSON serializzati separati da newline
                     - Eventi "progress": aggiornamenti sul progresso
                     - Evento "complete": risultato finale con flashcard
                     - Evento "error": in caso di errori durante l'elaborazione
            """
            # Inizializzazione delle variabili per l'elaborazione
            all_flashcards = []
            total_parts = len(merged_texts)
            
            # Elaborazione di ogni parte di testo estratto
            for i, text_part in enumerate(merged_texts):
                logger.info(f"Generazione flashcard per la parte {i+1}/{total_parts}")
                
                # Generazione flashcard per la porzione corrente di testo
                flashcards = generate_flashcards_from_text(text_part)
                all_flashcards.extend(flashcards)
                
                # Calcolo e invio del progresso corrente
                progress = {
                    "type": "progress",
                    "data": {
                        "current_part": i + 1,
                        "total_parts": total_parts,
                        "percentage": int(((i + 1) / total_parts) * 100)
                    }
                }
                
                # Invio dell'evento di progresso al client
                yield json.dumps(progress) + "\n"
                
                # Limite di sicurezza per evitare di generare troppe flashcard
                if len(all_flashcards) >= MAX_FLASHCARDS_LIMIT:
                    logger.info("Raggiunto limite massimo di flashcard")
                    break
            
            # Verifica che siano state generate almeno alcune flashcard
            if not all_flashcards:
                error = {
                    "type": "error",
                    "data": "Impossibile generare flashcard dal contenuto del PDF"
                }
                yield json.dumps(error) + "\n"
                return
            
            logger.info(f"Generate {len(all_flashcards)} flashcard totali")
            
            # Invio del risultato finale con tutte le flashcard e le statistiche
            result = {
                "type": "complete",
                "data": {
                    "flashcards": all_flashcards,
                    "statistics": {
                        "pages_processed": len(chunks),
                        "total_words": total_words,
                        "flashcards_generated": len(all_flashcards)
                    }
                }
            }
            yield json.dumps(result) + "\n"

        # Restituzione della risposta streaming con tipo MIME NDJSON
        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson"
        )
        
    except HTTPException:
        # Re-raise delle eccezioni HTTP per mantenere i codici di stato corretti
        raise
    except Exception as e:
        # Cattura e logging di tutti gli altri errori imprevisti
        logger.error(f"Errore durante l'elaborazione: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Endpoint per verificare lo stato di salute dell'applicazione.
    
    Controlla:
    - Disponibilità del servizio Ollama
    - Presenza del modello IA richiesto
    - Lista dei modelli disponibili
    
    Utilizzato per:
    - Monitoraggio dell'applicazione
    - Debugging dei problemi di configurazione
    - Verifica prima dell'elaborazione di documenti
    
    Returns:
        dict: Stato dettagliato dell'applicazione e dei servizi dipendenti
            - status: "healthy" | "unhealthy"
            - ollama_available: bool - Ollama raggiungibile
            - model_available: bool - Modello richiesto presente
            - models: list - Lista modelli disponibili
            - error: str | None - Dettagli errore se presente
    """
    # Verifica dello stato del servizio IA
    ollama_status = check_ollama_availability()
    
    # Restituzione dello stato completo dell'applicazione
    return {
        "status": "healthy" if ollama_status["available"] else "unhealthy",
        "ollama_available": ollama_status["available"],
        "model_available": ollama_status["model_available"],
        "models": ollama_status.get("models", []),
        "error": ollama_status.get("error")
    }

# Avvio dell'applicazione quando eseguita direttamente
if __name__ == "__main__":
    import uvicorn
    # Configurazione per lo sviluppo locale
    # host="0.0.0.0" permette connessioni da qualsiasi interfaccia di rete
    # port=8000 è la porta standard per il backend
    uvicorn.run(app, host="0.0.0.0", port=8000)