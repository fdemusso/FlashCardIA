from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import PyPDF2
import io
import ollama
from typing import List, Dict
import json
import logging
import re
import traceback
from dataclasses import dataclass
import asyncio

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configurazione CORS per lo sviluppo locale
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@dataclass
class TextChunk:
    content: str
    page_number: int
    word_count: int

def clean_text(text: str) -> str:
    """Pulisce il testo estratto dal PDF rimuovendo caratteri indesiderati e formattazioni problematiche."""
    if not text:
        return ""
    
    # Rimuovi caratteri di controllo e sostituisci con spazi
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', ' ', text)
    
    # Normalizza gli spazi bianchi
    text = re.sub(r'\s+', ' ', text)
    
    # Rimuovi linee con solo numeri (probabilmente numeri di pagina)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Rimuovi linee molto corte (meno di 3 caratteri)
    lines = text.split('\n')
    lines = [line.strip() for line in lines if len(line.strip()) > 3]
    
    # Ricongiunge le parole spezzate
    text = ' '.join(lines)
    
    # Rimuovi spazi multipli
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

def extract_text_from_pdf(pdf_file) -> List[TextChunk]:
    """Estrae il testo dal PDF dividendolo per pagine e creando chunks gestibili."""
    chunks = []
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        logger.info(f"PDF con {len(pdf_reader.pages)} pagine caricato")
        
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                # Estrai il testo dalla pagina
                raw_text = page.extract_text()
                
                if not raw_text or len(raw_text.strip()) < 10:
                    logger.warning(f"Pagina {page_num} contiene poco o nessun testo")
                    continue
                
                # Pulisci il testo
                cleaned_text = clean_text(raw_text)
                
                if len(cleaned_text) < 20:
                    logger.warning(f"Pagina {page_num} contiene testo insufficiente dopo la pulizia")
                    continue
                
                # Conta le parole
                word_count = len(cleaned_text.split())
                
                logger.info(f"Pagina {page_num}: {word_count} parole estratte")
                
                chunks.append(TextChunk(
                    content=cleaned_text,
                    page_number=page_num,
                    word_count=word_count
                ))
                
            except Exception as e:
                logger.error(f"Errore nell'estrazione del testo dalla pagina {page_num}: {str(e)}")
                continue
        
        return chunks
        
    except Exception as e:
        logger.error(f"Errore nella lettura del PDF: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Errore nella lettura del PDF: {str(e)}")

def merge_chunks_intelligently(chunks: List[TextChunk], max_words: int = 800) -> List[str]:
    """Unisce i chunks in modo intelligente per creare testi di dimensione ottimale per l'IA."""
    if not chunks:
        return []
    
    merged_texts = []
    current_text = ""
    current_word_count = 0
    
    for chunk in chunks:
        # Se aggiungendo questo chunk supereremmo il limite, salva il testo corrente
        if current_word_count + chunk.word_count > max_words and current_text:
            merged_texts.append(current_text.strip())
            current_text = chunk.content
            current_word_count = chunk.word_count
        else:
            # Aggiungi al testo corrente
            if current_text:
                current_text += "\n\n" + chunk.content
            else:
                current_text = chunk.content
            current_word_count += chunk.word_count
    
    # Aggiungi l'ultimo testo se presente
    if current_text.strip():
        merged_texts.append(current_text.strip())
    
    logger.info(f"Testo diviso in {len(merged_texts)} parti per l'elaborazione")
    return merged_texts

# Prompt ottimizzato per la generazione delle flashcard
FLASHCARD_PROMPT = """Crea 3-5 flashcard educative dal testo fornito.

REGOLE IMPORTANTI:
1. Rispondi ESCLUSIVAMENTE con un array JSON valido
2. NON aggiungere testo prima o dopo il JSON
3. NON usare markdown o backticks
4. Usa SOLO i tipi: "multipla", "vero_falso", "aperta"

FORMATO ESATTO:
[{{"domanda":"Testo domanda","risposta":"Risposta corretta","tipo":"multipla","opzioni":["Corretta","Sbagliata1","Sbagliata2","Sbagliata3"],"punteggio":3}},{{"domanda":"Domanda vero/falso","risposta":"vero","tipo":"vero_falso","punteggio":2}}]

TESTO DA ANALIZZARE:
{text}

Rispondi solo con JSON:"""

def generate_flashcards_from_text(text: str, model_name: str) -> List[Dict]:
    """Genera flashcard da un singolo testo usando Ollama."""
    try:
        logger.info(f"Generazione flashcard per testo di {len(text.split())} parole")
        
        # Prompt più semplice e diretto
        simple_prompt = f"""Analizza questo testo e crea 3 flashcard in formato JSON.
Per ogni flashcard, usa uno dei seguenti tipi:
- "aperta": per domande che richiedono una risposta libera
- "vero_falso": per affermazioni da verificare (risposta deve essere "vero" o "falso")
- "multipla": per domande con 4 opzioni di risposta (risposta deve essere una delle opzioni)

{text[:1000]}

Rispondi SOLO con array JSON senza markdown, per esempio:
[
  {{
    "domanda": "Qual è la capitale d'Italia?",
    "risposta": "Roma",
    "tipo": "aperta",
    "punteggio": 3
  }},
  {{
    "domanda": "La Terra è piatta",
    "risposta": "falso",
    "tipo": "vero_falso",
    "punteggio": 2
  }},
  {{
    "domanda": "Quale di questi è un pianeta?",
    "risposta": "Marte",
    "tipo": "multipla",
    "opzioni": ["Marte", "Luna", "Sole", "Stella"],
    "punteggio": 3
  }}
]

REGOLE IMPORTANTI:
1. Per tipo "multipla":
   - La risposta DEVE essere una delle opzioni fornite
   - Le opzioni devono essere 4
   - La risposta deve essere esattamente uguale a una delle opzioni
2. Per tipo "vero_falso":
   - La risposta DEVE essere esattamente "vero" o "falso"
3. Per tipo "aperta":
   - La risposta può essere qualsiasi testo"""

        logger.info(f"Invio prompt a Ollama (lunghezza: {len(simple_prompt)} caratteri)")
        
        response = ollama.generate(
            model=model_name,
            prompt=simple_prompt,
            stream=False,
            options={
                "temperature": 0.1,
                "num_predict": 1000
            }
        )
        
        logger.info(f"Risposta grezza da Ollama: {response}")
        
        if not response or 'response' not in response:
            logger.error("Risposta non valida da Ollama")
            return []
        
        response_text = response['response']
        logger.info(f"Risposta ricevuta ({len(response_text)} caratteri): {response_text}")
        
        if not response_text or len(response_text.strip()) == 0:
            logger.error("Risposta vuota da Ollama")
            return []
        
        # Pulisci la risposta per estrarre solo il JSON
        response_text = clean_json_response(response_text)
        logger.info(f"JSON pulito: {response_text}")
        
        if not response_text or response_text == "[]":
            logger.error("Nessun JSON valido trovato nella risposta")
            return []
        
        try:
            flashcards = json.loads(response_text)
            
            if not isinstance(flashcards, list):
                flashcards = [flashcards] if isinstance(flashcards, dict) else []
            
            # Valida le flashcard
            valid_flashcards = validate_flashcards(flashcards)
            logger.info(f"Generate {len(valid_flashcards)} flashcard valide")
            
            return valid_flashcards
            
        except json.JSONDecodeError as e:
            logger.error(f"Errore nel parsing JSON: {str(e)}")
            logger.error(f"Testo problematico: {response_text}")
            
            # Tentativo di recupero con regex più semplice
            try:
                import re
                # Cerca un array JSON semplice
                json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(0)
                    logger.info(f"Trovato JSON con regex: {json_text}")
                    flashcards = json.loads(json_text)
                    if isinstance(flashcards, list):
                        return validate_flashcards(flashcards)
            except Exception as recovery_error:
                logger.error(f"Errore nel tentativo di recupero: {recovery_error}")
            
            return []
            
    except Exception as e:
        logger.error(f"Errore nella generazione flashcard: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []

def clean_json_response(response_text: str) -> str:
    """Pulisce la risposta per estrarre solo il JSON valido."""
    
    # Rimuovi possibili prefissi comuni
    response_text = re.sub(r'^(```json\s*|```\s*|JSON:\s*|Risposta:\s*)', '', response_text, flags=re.IGNORECASE)
    response_text = re.sub(r'(```\s*|```json\s*)$', '', response_text, flags=re.IGNORECASE)
    
    # Trova il primo [ e l'ultimo ]
    start_idx = response_text.find('[')
    end_idx = response_text.rfind(']')
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        # Prova a trovare un singolo oggetto JSON e lo wrappa in array
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            logger.error("Nessun JSON trovato nella risposta")
            return "[]"
        
        # Wrappa l'oggetto singolo in un array
        single_object = response_text[start_idx:end_idx + 1]
        return f"[{single_object}]"
    
    json_text = response_text[start_idx:end_idx + 1]
    
    # Rimuovi commenti e testo extra
    json_text = re.sub(r'//.*?\n', '', json_text)
    json_text = re.sub(r'/\*.*?\*/', '', json_text, flags=re.DOTALL)
    
    # Rimuovi possibili caratteri non stampabili
    json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
    
    return json_text.strip()

def validate_flashcards(flashcards: List[Dict]) -> List[Dict]:
    """Valida e pulisce le flashcard generate."""
    valid_flashcards = []
    
    for i, card in enumerate(flashcards):
        try:
            # Verifica campi obbligatori
            required_fields = ["domanda", "risposta", "tipo", "punteggio"]
            if not all(field in card for field in required_fields):
                logger.warning(f"Flashcard {i} manca di campi obbligatori: {card}")
                continue
            
            # Verifica tipo valido
            if card["tipo"] not in ["multipla", "vero_falso", "aperta"]:
                logger.warning(f"Flashcard {i} ha tipo non valido: {card['tipo']}")
                continue
            
            # Verifica punteggio
            if not isinstance(card["punteggio"], int) or not 1 <= card["punteggio"] <= 5:
                card["punteggio"] = 3  # Default
            
            # Verifica domande multiple
            if card["tipo"] == "multipla":
                if "opzioni" not in card or not isinstance(card["opzioni"], list) or len(card["opzioni"]) < 2:
                    logger.warning(f"Flashcard multipla {i} non ha opzioni valide")
                    continue
                
                # Assicurati che ci siano 4 opzioni
                if len(card["opzioni"]) < 4:
                    # Aggiungi opzioni dummy se necessario
                    while len(card["opzioni"]) < 4:
                        card["opzioni"].append(f"Opzione {len(card['opzioni']) + 1}")
                elif len(card["opzioni"]) > 4:
                    card["opzioni"] = card["opzioni"][:4]
            
            # Pulisci testi
            card["domanda"] = str(card["domanda"]).strip()
            card["risposta"] = str(card["risposta"]).strip()
            
            if len(card["domanda"]) < 5 or len(card["risposta"]) < 1:
                logger.warning(f"Flashcard {i} ha testi troppo corti")
                continue
            
            valid_flashcards.append(card)
            
        except Exception as e:
            logger.error(f"Errore nella validazione della flashcard {i}: {str(e)}")
            continue
    
    return valid_flashcards

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
        
        if total_words < 50:
            raise HTTPException(status_code=400, detail="Il PDF contiene troppo poco testo per generare flashcard significative.")
        
        # Unisci i chunks in modo intelligente
        merged_texts = merge_chunks_intelligently(chunks, max_words=800)
        
        # Verifica che Ollama sia disponibile
        logger.info("Verifica disponibilità Ollama...")
        try:
            models = ollama.list()
            model_name = 'gemma3:4b-it-qat'
            
            if not any(model['name'] == model_name for model in models['models']):
                logger.error(f"Modello {model_name} non trovato")
                raise HTTPException(status_code=500, detail=f"Modello {model_name} non disponibile")
            
            logger.info(f"Modello {model_name} disponibile")
            
        except Exception as e:
            logger.error(f"Errore nella verifica di Ollama: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Servizio IA non disponibile: {str(e)}")

        async def generate():
            # Genera flashcard per ogni parte di testo
            all_flashcards = []
            total_parts = len(merged_texts)
            
            for i, text_part in enumerate(merged_texts):
                logger.info(f"Generazione flashcard per la parte {i+1}/{len(merged_texts)}")
                
                flashcards = generate_flashcards_from_text(text_part, model_name)
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
                if len(all_flashcards) >= 20:
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
    try:
        # Verifica Ollama
        models = ollama.list()
        model_available = any(model['name'] == 'gemma3:4b-it-qat' for model in models['models'])
        
        return {
            "status": "healthy",
            "ollama_available": True,
            "model_available": model_available,
            "models": [model['name'] for model in models['models']]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "ollama_available": False
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)