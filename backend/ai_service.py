import ollama
import json
import re
import logging
import traceback
from typing import List, Dict

from config import AI_MODEL_NAME, OLLAMA_OPTIONS
from validation import validate_flashcards

logger = logging.getLogger(__name__)

def generate_flashcards_from_text(text: str, model_name: str = AI_MODEL_NAME) -> List[Dict]:
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
            options=OLLAMA_OPTIONS
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

def check_ollama_availability() -> Dict:
    """Verifica se Ollama è disponibile e se il modello richiesto è presente."""
    try:
        models = ollama.list()
        model_available = any(model['name'] == AI_MODEL_NAME for model in models['models'])
        
        return {
            "available": True,
            "model_available": model_available,
            "models": [model['name'] for model in models['models']]
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "model_available": False
        } 