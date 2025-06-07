"""
Servizio di Intelligenza Artificiale per la generazione di flashcard.

Questo modulo gestisce l'interazione con Ollama (servizio IA locale) per:
- Generare flashcard educative da testo estratto da PDF
- Validare e pulire le risposte dall'IA
- Verificare la disponibilità del servizio e dei modelli
- Gestire errori e fallback per risposte malformate

Il servizio supporta tre tipi di flashcard:
- Domande aperte: Richiedono risposte libere
- Vero/Falso: Affermazioni da verificare
- Multiple choice: Domande con 4 opzioni di risposta

Ogni flashcard include:
- Domanda e risposta
- Punteggio di difficoltà (1-5)
- Giustificazione (per domande chiuse)
"""

import ollama
import json
import re
import logging
import traceback
from typing import List, Dict

from config import AI_MODEL_NAME, OLLAMA_OPTIONS
from validation import validate_flashcards

# Configurazione del logger per tracciare le operazioni IA
logger = logging.getLogger(__name__)

def generate_flashcards_from_text(text: str, model_name: str = AI_MODEL_NAME) -> List[Dict]:
    """
    Genera flashcard educative dal testo fornito utilizzando l'IA locale (Ollama).
    
    Questa funzione:
    1. Prepara un prompt ottimizzato per la generazione di flashcard
    2. Invia il testo a Ollama per l'elaborazione
    3. Pulisce e valida la risposta JSON ricevuta
    4. Applica validazioni e correzioni alle flashcard generate
    
    Args:
        text (str): Testo da cui generare le flashcard (estratto da PDF)
        model_name (str): Nome del modello Ollama da utilizzare (default da config)
    
    Returns:
        List[Dict]: Lista di flashcard validate, ogni dict contiene:
            - domanda (str): La domanda formulata
            - risposta (str/int): La risposta corretta
            - tipo (str): Tipo di domanda ('aperta', 'vero_falso', 'multipla')
            - punteggio (int): Difficoltà da 1 a 5
            - opzioni (List[str], opzionale): Opzioni per domande multiple choice
            - giustificazione (str, opzionale): Spiegazione per domande chiuse
    
    Raises:
        Exception: Per errori di comunicazione con Ollama o parsing JSON
    """
    try:
        logger.info(f"Generazione flashcard per testo di {len(text.split())} parole")
        
        # Costruzione del prompt ottimizzato per Ollama
        # Il prompt è specificamente progettato per:
        # - Generare esattamente 3 flashcard per chiamata
        # - Utilizzare formato JSON strutturato
        # - Includere giustificazioni per domande chiuse
        # - Gestire correttamente gli indici per multiple choice
        simple_prompt = f"""Analizza questo testo e crea 3 flashcard in formato JSON.
Per ogni flashcard, usa uno dei seguenti tipi:
- "aperta": per domande che richiedono una risposta libera
- "vero_falso": per affermazioni da verificare (risposta deve essere "vero" o "falso")
- "multipla": per domande con 4 opzioni di risposta (risposta deve essere l'INDICE dell'opzione corretta: 0, 1, 2, o 3)

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
    "punteggio": 2,
    "giustificazione": "La Terra ha una forma sferica, come dimostrato da secoli di osservazioni astronomiche e prove scientifiche"
  }},
  {{
    "domanda": "Quale di questi è un pianeta?",
    "risposta": 0,
    "tipo": "multipla",
    "opzioni": ["Marte", "Luna", "Sole", "Stella"],
    "punteggio": 3,
    "giustificazione": "Marte è l'unico pianeta tra le opzioni. La Luna è un satellite, il Sole è una stella e 'Stella' è una categoria generale di corpi celesti"
  }}
]

REGOLE IMPORTANTI:
1. Per tipo "multipla":
   - La risposta DEVE essere un numero (0, 1, 2, o 3) che rappresenta l'indice dell'opzione corretta
   - Le opzioni devono essere 4
   - L'indice 0 corrisponde alla prima opzione, 1 alla seconda, ecc.
   - AGGIUNGI sempre il campo "giustificazione" che spiega perché quella è la risposta corretta
2. Per tipo "vero_falso":
   - La risposta DEVE essere esattamente "vero" o "falso"
   - AGGIUNGI sempre il campo "giustificazione" che spiega perché l'affermazione è vera o falsa
3. Per tipo "aperta":
   - La risposta può essere qualsiasi testo
   - NON aggiungere il campo "giustificazione" per questo tipo"""

        logger.info(f"Invio prompt a Ollama (lunghezza: {len(simple_prompt)} caratteri)")
        
        # Invio del prompt al modello IA con configurazione ottimizzata
        response = ollama.generate(
            model=model_name,
            prompt=simple_prompt,
            stream=False,           # Disabilita streaming per ricevere risposta completa
            options=OLLAMA_OPTIONS  # Configurazione da config.py (temperatura, token limit)
        )
        
        logger.info(f"Risposta grezza da Ollama: {response}")
        
        # Verifica che la risposta sia valida e contenga il campo 'response'
        if not response or 'response' not in response:
            logger.error("Risposta non valida da Ollama")
            return []
        
        response_text = response['response']
        logger.info(f"Risposta ricevuta ({len(response_text)} caratteri): {response_text}")
        
        # Verifica che la risposta non sia vuota
        if not response_text or len(response_text.strip()) == 0:
            logger.error("Risposta vuota da Ollama")
            return []
        
        # Pulizia della risposta per estrarre solo il JSON valido
        response_text = clean_json_response(response_text)
        logger.info(f"JSON pulito: {response_text}")
        
        # Verifica che dopo la pulizia ci sia ancora contenuto valido
        if not response_text or response_text == "[]":
            logger.error("Nessun JSON valido trovato nella risposta")
            return []
        
        try:
            # Parsing del JSON per ottenere le flashcard
            flashcards = json.loads(response_text)
            
            # Assicuriamoci che il risultato sia sempre una lista
            if not isinstance(flashcards, list):
                flashcards = [flashcards] if isinstance(flashcards, dict) else []
            
            # Applicazione delle validazioni e correzioni alle flashcard
            valid_flashcards = validate_flashcards(flashcards)
            logger.info(f"Generate {len(valid_flashcards)} flashcard valide")
            
            return valid_flashcards
            
        except json.JSONDecodeError as e:
            # Gestione degli errori di parsing JSON con tentativo di recupero
            logger.error(f"Errore nel parsing JSON: {str(e)}")
            logger.error(f"Testo problematico: {response_text}")
            
            # Tentativo di recupero con regex più semplice
            try:
                # Cerca un array JSON semplice nella risposta
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
        # Logging completo per debugging di errori imprevisti
        logger.error(f"Errore nella generazione flashcard: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []

def clean_json_response(response_text: str) -> str:
    """
    Pulisce la risposta testuale dall'IA per estrarre JSON valido.
    
    L'IA può restituire risposte con formattazione extra come:
    - Blocchi di codice markdown (```json...```)
    - Prefissi descrittivi ("Risposta:", "JSON:")
    - Commenti e testo aggiuntivo
    - Caratteri non stampabili
    
    Questa funzione:
    1. Rimuove prefissi e suffissi comuni
    2. Estrae il contenuto JSON (array [...] o oggetto {...})
    3. Pulisce commenti e caratteri problematici
    4. Gestisce sia array che singoli oggetti
    
    Args:
        response_text (str): Risposta grezza dall'IA
    
    Returns:
        str: JSON pulito e validato, o "[]" se non trovato JSON valido
    """
    
    # Rimozione di prefissi comuni nelle risposte IA
    response_text = re.sub(r'^(```json\s*|```\s*|JSON:\s*|Risposta:\s*)', '', response_text, flags=re.IGNORECASE)
    response_text = re.sub(r'(```\s*|```json\s*)$', '', response_text, flags=re.IGNORECASE)
    
    # Ricerca del primo [ e dell'ultimo ] per array JSON
    start_idx = response_text.find('[')
    end_idx = response_text.rfind(']')
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        # Se non trovato array, cerca un singolo oggetto JSON e lo wrappa
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            logger.error("Nessun JSON trovato nella risposta")
            return "[]"
        
        # Wrapping dell'oggetto singolo in un array
        single_object = response_text[start_idx:end_idx + 1]
        return f"[{single_object}]"
    
    # Estrazione del contenuto JSON dell'array
    json_text = response_text[start_idx:end_idx + 1]
    
    # Rimozione di commenti JavaScript-style che possono interferire
    json_text = re.sub(r'//.*?\n', '', json_text)
    json_text = re.sub(r'/\*.*?\*/', '', json_text, flags=re.DOTALL)
    
    # Rimozione di caratteri non stampabili che possono causare errori di parsing
    json_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_text)
    
    return json_text.strip()

def check_ollama_availability() -> Dict:
    """
    Verifica la disponibilità del servizio Ollama e del modello richiesto.
    
    Questa funzione:
    1. Tenta di connettersi al servizio Ollama locale
    2. Recupera la lista dei modelli installati
    3. Verifica che il modello specificato in config sia disponibile
    4. Restituisce informazioni dettagliate sullo stato
    
    Utilizzata per:
    - Health check dell'applicazione
    - Verifica prerequisiti prima dell'elaborazione
    - Debugging di problemi di configurazione
    
    Returns:
        Dict: Dizionario con informazioni sullo stato:
            - available (bool): Ollama è raggiungibile
            - model_available (bool): Il modello richiesto è presente
            - models (List[str]): Lista dei modelli installati
            - error (str, opzionale): Messaggio di errore se presente
    
    Note:
        Non solleva eccezioni, restituisce sempre un dizionario con le informazioni
        disponibili. Gli errori sono catturati e riportati nel campo 'error'.
    """
    try:
        # Tentativo di connessione a Ollama per ottenere la lista dei modelli
        models = ollama.list()
        
        # Verifica che il modello specificato in config sia tra quelli disponibili
        model_available = any(model['name'] == AI_MODEL_NAME for model in models['models'])
        
        # Restituzione dello stato positivo con dettagli
        return {
            "available": True,
            "model_available": model_available,
            "models": [model['name'] for model in models['models']]
        }
    except Exception as e:
        # Cattura di tutti gli errori (connessione, timeout, etc.)
        # e restituzione dello stato negativo con dettagli dell'errore
        return {
            "available": False,
            "error": str(e),
            "model_available": False
        } 