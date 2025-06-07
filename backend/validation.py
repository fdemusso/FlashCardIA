"""
Sistema di validazione e correzione per le flashcard generate dall'IA.

Questo modulo gestisce la validazione, pulizia e correzione delle flashcard
generate dal servizio di intelligenza artificiale. Assicura che:
- Tutte le flashcard abbiano i campi obbligatori
- I tipi di domande siano validi e coerenti
- Le risposte siano nel formato corretto
- Le opzioni multiple choice siano complete e coerenti
- I testi siano puliti e di lunghezza adeguata

Il sistema implementa correzioni automatiche quando possibile e scarta
le flashcard che non possono essere riparate, garantendo qualità e coerenza.
"""

import logging
from typing import List, Dict

from config import (
    VALID_CARD_TYPES, 
    DEFAULT_SCORE, 
    MIN_QUESTION_LENGTH, 
    MIN_ANSWER_LENGTH, 
    MULTIPLE_CHOICE_OPTIONS_COUNT
)

# Configurazione del logger per tracciare le operazioni di validazione
logger = logging.getLogger(__name__)

def validate_flashcards(flashcards: List[Dict]) -> List[Dict]:
    """
    Valida e corregge una lista di flashcard generate dall'IA.
    
    Questa funzione è il punto di ingresso principale per la validazione.
    Per ogni flashcard nella lista, esegue una serie di controlli e correzioni:
    
    1. Verifica presenza campi obbligatori
    2. Valida il tipo di domanda
    3. Assegna punteggio di default se mancante/invalido
    4. Gestisce specificamente domande multiple choice
    5. Gestisce specificamente domande vero/falso
    6. Pulisce i testi da spazi e formattazione
    7. Verifica lunghezze minime
    
    Args:
        flashcards (List[Dict]): Lista di flashcard grezze dall'IA
    
    Returns:
        List[Dict]: Lista di flashcard validate e corrette
        
    Note:
        Le flashcard che non possono essere corrette vengono scartate.
        Il processo è logged per debugging e monitoraggio della qualità.
    """
    valid_flashcards = []
    
    # Elaborazione di ogni flashcard individualmente
    for i, card in enumerate(flashcards):
        try:
            # Controllo 1: Verifica presenza campi obbligatori
            required_fields = ["domanda", "risposta", "tipo"]
            if not all(field in card for field in required_fields):
                logger.warning(f"Flashcard {i} manca di campi obbligatori: {card}")
                continue
            
            # Controllo 2: Verifica che il tipo sia tra quelli supportati
            if card["tipo"] not in VALID_CARD_TYPES:
                logger.warning(f"Flashcard {i} ha tipo non valido: {card['tipo']}")
                continue
            
            # Controllo 3: Verifica/assegnazione punteggio di difficoltà
            if "punteggio" not in card or not isinstance(card["punteggio"], int) or not 1 <= card["punteggio"] <= 5:
                card["punteggio"] = DEFAULT_SCORE  # Assegna punteggio di default
                logger.info(f"Flashcard {i}: assegnato punteggio default {DEFAULT_SCORE}")
            
            # Controllo 4: Gestione specifica per domande multiple choice
            if card["tipo"] == "multipla":
                if not _validate_multiple_choice(card, i):
                    continue  # Scarta se non validabile
            
            # Controllo 5: Gestione specifica per domande vero/falso
            if card["tipo"] == "vero_falso":
                if not _validate_true_false(card, i):
                    continue  # Scarta se non validabile
            
            # Controllo 6: Pulizia specifica per domande aperte
            if card["tipo"] == "aperta":
                _clean_open_question(card)
            
            # Controllo 7: Pulizia generale dei testi
            _clean_texts(card)
            
            # Controllo 8: Verifica lunghezze minime
            if len(card["domanda"]) < MIN_QUESTION_LENGTH or len(card["risposta"]) < MIN_ANSWER_LENGTH:
                logger.warning(f"Flashcard {i} ha testi troppo corti")
                continue
            
            # Se tutti i controlli sono passati, aggiungi alla lista valida
            valid_flashcards.append(card)
            
        except Exception as e:
            # Cattura errori imprevisti durante la validazione
            logger.error(f"Errore nella validazione della flashcard {i}: {str(e)}")
            continue
    
    return valid_flashcards

def _validate_multiple_choice(card: Dict, index: int) -> bool:
    """
    Valida e corregge una flashcard di tipo multiple choice.
    
    Controlli specifici per domande multiple choice:
    - Presenza e validità delle opzioni
    - Numero corretto di opzioni (4)
    - Coerenza tra risposta e opzioni
    - Presenza della giustificazione
    
    Args:
        card (Dict): Flashcard da validare (modificata in-place)
        index (int): Indice per logging
    
    Returns:
        bool: True se la flashcard è valida/riparabile, False altrimenti
    """
    # Verifica presenza e validità delle opzioni
    if "opzioni" not in card or not isinstance(card["opzioni"], list) or len(card["opzioni"]) < 2:
        logger.warning(f"Flashcard multipla {index} non ha opzioni valide")
        return False
    
    # Normalizzazione del numero di opzioni a 4
    if len(card["opzioni"]) < MULTIPLE_CHOICE_OPTIONS_COUNT:
        # Aggiungi opzioni dummy se necessario
        while len(card["opzioni"]) < MULTIPLE_CHOICE_OPTIONS_COUNT:
            card["opzioni"].append(f"Opzione {len(card['opzioni']) + 1}")
    elif len(card["opzioni"]) > MULTIPLE_CHOICE_OPTIONS_COUNT:
        # Tronca a 4 opzioni se ce ne sono troppe
        card["opzioni"] = card["opzioni"][:MULTIPLE_CHOICE_OPTIONS_COUNT]
    
    # Gestione dell'indice della risposta
    try:
        # Se la risposta è un numero (indice), convertila nel testo dell'opzione
        if isinstance(card["risposta"], (int, float)):
            response_index = int(card["risposta"])
            if 0 <= response_index < len(card["opzioni"]):
                card["risposta"] = card["opzioni"][response_index]
                logger.info(f"Flashcard multipla {index}: convertito indice {response_index} in '{card['risposta']}'")
            else:
                logger.warning(f"Flashcard multipla {index} ha indice risposta non valido: {response_index}")
                return False
        
        # Verifica che la risposta sia ora tra le opzioni disponibili
        if card["risposta"] not in card["opzioni"]:
            logger.warning(f"Flashcard multipla {index} ha risposta non corrispondente alle opzioni: {card['risposta']} non in {card['opzioni']}")
            return False
            
    except (ValueError, TypeError) as e:
        logger.warning(f"Flashcard multipla {index} ha risposta non convertibile: {card['risposta']}")
        return False
    
    # Verifica presenza della giustificazione (obbligatoria per multiple choice)
    if "giustificazione" not in card or not card["giustificazione"]:
        logger.warning(f"Flashcard multipla {index} manca della giustificazione")
        card["giustificazione"] = "Giustificazione non disponibile"
    
    return True

def _validate_true_false(card: Dict, index: int) -> bool:
    """
    Valida e corregge una flashcard di tipo vero/falso.
    
    Controlli specifici per domande vero/falso:
    - Risposta deve essere esattamente "vero" o "falso"
    - Presenza della giustificazione (obbligatoria)
    
    Args:
        card (Dict): Flashcard da validare (modificata in-place)
        index (int): Indice per logging
    
    Returns:
        bool: True se la flashcard è valida, False altrimenti
    """
    # Verifica che la risposta sia vero o falso
    if card["risposta"].lower() not in ["vero", "falso"]:
        logger.warning(f"Flashcard vero/falso {index} ha risposta non valida: {card['risposta']}")
        return False
    
    # Normalizza la risposta (lowercase)
    card["risposta"] = card["risposta"].lower()
    
    # Verifica presenza della giustificazione (obbligatoria per vero/falso)
    if "giustificazione" not in card or not card["giustificazione"]:
        logger.warning(f"Flashcard vero/falso {index} manca della giustificazione")
        card["giustificazione"] = "Giustificazione non disponibile"
    
    return True

def _clean_open_question(card: Dict) -> None:
    """
    Pulisce una flashcard di tipo domanda aperta.
    
    Per le domande aperte:
    - Rimuove il campo giustificazione se presente (non necessario)
    - Rimuove il campo opzioni se presente (non utilizzato)
    
    Args:
        card (Dict): Flashcard da pulire (modificata in-place)
    """
    # Per domande aperte, rimuovi campi non necessari
    if "giustificazione" in card:
        del card["giustificazione"]
    
    if "opzioni" in card:
        del card["opzioni"]

def _clean_texts(card: Dict) -> None:
    """
    Pulisce i testi di una flashcard da spazi e formattazione indesiderata.
    
    Operazioni di pulizia:
    - Rimozione spazi iniziali e finali
    - Conversione a stringa (safety check)
    - Pulizia della giustificazione se presente
    
    Args:
        card (Dict): Flashcard da pulire (modificata in-place)
    """
    # Pulizia dei campi di testo principali
    card["domanda"] = str(card["domanda"]).strip()
    card["risposta"] = str(card["risposta"]).strip()
    
    # Pulizia della giustificazione se presente
    if "giustificazione" in card:
        card["giustificazione"] = str(card["giustificazione"]).strip() 