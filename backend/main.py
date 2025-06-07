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

logger = logging.getLogger(__name__)

app = FastAPI()

# Configurazione CORS per lo sviluppo locale
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Verifica che sia un PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Il file deve essere un PDF")
        
        # Leggi il contenuto del PDF
        content = await file.read()
        pdf_file = io.BytesIO(content)
        
        # Estrai il testo dal PDF per pagine
        logger.info("Inizio estrazione testo dal PDF...")
        chunks = extract_text_from_pdf(pdf_file)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Impossibile estrarre testo dal PDF. Il file potrebbe essere un'immagine o essere danneggiato.")
        
        # Calcola statistiche
        total_words = sum(chunk.word_count for chunk in chunks)
        logger.info(f"Estratto testo da {len(chunks)} pagine, totale {total_words} parole")
        
        if total_words < MIN_WORDS_FOR_PROCESSING:
            raise HTTPException(status_code=400, detail="Il PDF contiene troppo poco testo per generare flashcard significative.")
        
        # Unisci i chunks in modo intelligente
        merged_texts = merge_chunks_intelligently(chunks)
        
        # Verifica che Ollama sia disponibile
        logger.info("Verifica disponibilità Ollama...")
        ollama_status = check_ollama_availability()
        
        if not ollama_status["available"]:
            raise HTTPException(status_code=500, detail=f"Servizio IA non disponibile: {ollama_status.get('error', 'Errore sconosciuto')}")
        
        if not ollama_status["model_available"]:
            raise HTTPException(status_code=500, detail="Modello IA richiesto non disponibile")
        
        logger.info("Modello IA disponibile")

        async def generate():
            # Genera flashcard per ogni parte di testo
            all_flashcards = []
            total_parts = len(merged_texts)
            
            for i, text_part in enumerate(merged_texts):
                logger.info(f"Generazione flashcard per la parte {i+1}/{total_parts}")
                
                flashcards = generate_flashcards_from_text(text_part)
                all_flashcards.extend(flashcards)
                
                # Calcola il progresso
                progress = {
                    "type": "progress",
                    "data": {
                        "current_part": i + 1,
                        "total_parts": total_parts,
                        "percentage": int(((i + 1) / total_parts) * 100)
                    }
                }
                
                # Invia il progresso
                yield json.dumps(progress) + "\n"
                
                # Limite di sicurezza per evitare troppe flashcard
                if len(all_flashcards) >= MAX_FLASHCARDS_LIMIT:
                    logger.info("Raggiunto limite massimo di flashcard")
                    break
            
            if not all_flashcards:
                error = {
                    "type": "error",
                    "data": "Impossibile generare flashcard dal contenuto del PDF"
                }
                yield json.dumps(error) + "\n"
                return
            
            logger.info(f"Generate {len(all_flashcards)} flashcard totali")
            
            # Invia il risultato finale
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

        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione: {str(e)}")

@app.get("/health")
async def health_check():
    """Endpoint per verificare lo stato del servizio."""
    ollama_status = check_ollama_availability()
    
    return {
        "status": "healthy" if ollama_status["available"] else "unhealthy",
        "ollama_available": ollama_status["available"],
        "model_available": ollama_status["model_available"],
        "models": ollama_status.get("models", []),
        "error": ollama_status.get("error")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)