import logging
from typing import List, Dict

from config import (
    VALID_CARD_TYPES, 
    DEFAULT_SCORE, 
    MIN_QUESTION_LENGTH, 
    MIN_ANSWER_LENGTH, 
    MULTIPLE_CHOICE_OPTIONS_COUNT
)

logger = logging.getLogger(__name__)

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
            if card["tipo"] not in VALID_CARD_TYPES:
                logger.warning(f"Flashcard {i} ha tipo non valido: {card['tipo']}")
                continue
            
            # Verifica punteggio
            if not isinstance(card["punteggio"], int) or not 1 <= card["punteggio"] <= 5:
                card["punteggio"] = DEFAULT_SCORE  # Default
            
            # Verifica domande multiple
            if card["tipo"] == "multipla":
                if "opzioni" not in card or not isinstance(card["opzioni"], list) or len(card["opzioni"]) < 2:
                    logger.warning(f"Flashcard multipla {i} non ha opzioni valide")
                    continue
                
                # Assicurati che ci siano 4 opzioni
                if len(card["opzioni"]) < MULTIPLE_CHOICE_OPTIONS_COUNT:
                    # Aggiungi opzioni dummy se necessario
                    while len(card["opzioni"]) < MULTIPLE_CHOICE_OPTIONS_COUNT:
                        card["opzioni"].append(f"Opzione {len(card['opzioni']) + 1}")
                elif len(card["opzioni"]) > MULTIPLE_CHOICE_OPTIONS_COUNT:
                    card["opzioni"] = card["opzioni"][:MULTIPLE_CHOICE_OPTIONS_COUNT]
            
            # Pulisci testi
            card["domanda"] = str(card["domanda"]).strip()
            card["risposta"] = str(card["risposta"]).strip()
            
            if len(card["domanda"]) < MIN_QUESTION_LENGTH or len(card["risposta"]) < MIN_ANSWER_LENGTH:
                logger.warning(f"Flashcard {i} ha testi troppo corti")
                continue
            
            valid_flashcards.append(card)
            
        except Exception as e:
            logger.error(f"Errore nella validazione della flashcard {i}: {str(e)}")
            continue
    
    return valid_flashcards 