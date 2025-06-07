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
            required_fields = ["domanda", "risposta", "tipo"]
            if not all(field in card for field in required_fields):
                logger.warning(f"Flashcard {i} manca di campi obbligatori: {card}")
                continue
            
            # Verifica tipo valido
            if card["tipo"] not in VALID_CARD_TYPES:
                logger.warning(f"Flashcard {i} ha tipo non valido: {card['tipo']}")
                continue
            
            # Verifica/assegna punteggio
            if "punteggio" not in card or not isinstance(card["punteggio"], int) or not 1 <= card["punteggio"] <= 5:
                card["punteggio"] = DEFAULT_SCORE  # Default
                logger.info(f"Flashcard {i}: assegnato punteggio default {DEFAULT_SCORE}")
            
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
                
                # Gestione dell'indice della risposta
                try:
                    # Se la risposta è un numero (indice), convertila nel testo dell'opzione
                    if isinstance(card["risposta"], (int, float)):
                        response_index = int(card["risposta"])
                        if 0 <= response_index < len(card["opzioni"]):
                            card["risposta"] = card["opzioni"][response_index]
                            logger.info(f"Flashcard multipla {i}: convertito indice {response_index} in '{card['risposta']}'")
                        else:
                            logger.warning(f"Flashcard multipla {i} ha indice risposta non valido: {response_index}")
                            continue
                    
                    # Verifica che la risposta sia ora tra le opzioni
                    if card["risposta"] not in card["opzioni"]:
                        logger.warning(f"Flashcard multipla {i} ha risposta non corrispondente alle opzioni: {card['risposta']} non in {card['opzioni']}")
                        continue
                        
                except (ValueError, TypeError) as e:
                    logger.warning(f"Flashcard multipla {i} ha risposta non convertibile: {card['risposta']}")
                    continue
                
                # Verifica che esista la giustificazione per domande multiple
                if "giustificazione" not in card or not card["giustificazione"]:
                    logger.warning(f"Flashcard multipla {i} manca della giustificazione")
                    card["giustificazione"] = "Giustificazione non disponibile"
            
            # Verifica domande vero/falso
            if card["tipo"] == "vero_falso":
                # Verifica che la risposta sia vero o falso
                if card["risposta"].lower() not in ["vero", "falso"]:
                    logger.warning(f"Flashcard vero/falso {i} ha risposta non valida: {card['risposta']}")
                    continue
                
                # Verifica che esista la giustificazione per domande vero/falso
                if "giustificazione" not in card or not card["giustificazione"]:
                    logger.warning(f"Flashcard vero/falso {i} manca della giustificazione")
                    card["giustificazione"] = "Giustificazione non disponibile"
            
            # Per domande aperte, rimuovi il campo giustificazione se presente
            if card["tipo"] == "aperta":
                if "giustificazione" in card:
                    del card["giustificazione"]
            
            # Pulisci testi
            card["domanda"] = str(card["domanda"]).strip()
            card["risposta"] = str(card["risposta"]).strip()
            
            # Pulisci giustificazione se presente
            if "giustificazione" in card:
                card["giustificazione"] = str(card["giustificazione"]).strip()
            
            if len(card["domanda"]) < MIN_QUESTION_LENGTH or len(card["risposta"]) < MIN_ANSWER_LENGTH:
                logger.warning(f"Flashcard {i} ha testi troppo corti")
                continue
            
            valid_flashcards.append(card)
            
        except Exception as e:
            logger.error(f"Errore nella validazione della flashcard {i}: {str(e)}")
            continue
    
    return valid_flashcards 