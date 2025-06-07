"""
Modelli di dati per l'applicazione Generatore di Flashcard IA.

Questo modulo definisce le strutture dati utilizzate in tutta l'applicazione
per rappresentare:
- Porzioni di testo estratte dai PDF
- Dati delle flashcard generate
- Statistiche di elaborazione
- Informazioni sul progresso delle operazioni

Utilizza dataclasses per creare strutture dati immutabili e type-safe,
facilitando la serializzazione/deserializzazione e la validazione dei dati.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class TextChunk:
    """
    Rappresenta una porzione di testo estratta da un documento PDF.
    
    Ogni chunk corrisponde tipicamente a una pagina del PDF e contiene
    il testo pulito insieme ai metadati necessari per il tracciamento
    e l'elaborazione successiva.
    
    Attributes:
        content (str): Il testo estratto e pulito dalla pagina
        page_number (int): Numero della pagina di origine (1-based)
        word_count (int): Numero di parole contenute nel testo
    
    Usage:
        chunk = TextChunk(
            content="Questo è il testo della pagina...",
            page_number=1,
            word_count=150
        )
    """
    content: str        # Testo estratto e pulito dalla pagina PDF
    page_number: int    # Numero della pagina di origine (inizia da 1)
    word_count: int     # Conteggio delle parole per statistiche e chunking

@dataclass
class FlashcardData:
    """
    Struttura dati per una singola flashcard educativa.
    
    Rappresenta una flashcard completa con tutti i suoi componenti:
    domanda, risposta, tipo, difficoltà e informazioni aggiuntive.
    Supporta tre tipi di flashcard: aperte, vero/falso e multiple choice.
    
    Attributes:
        domanda (str): La domanda formulata dall'IA
        risposta (str): La risposta corretta
        tipo (str): Tipo di flashcard ('aperta', 'vero_falso', 'multipla')
        punteggio (int): Livello di difficoltà da 1 (facile) a 5 (difficile)
        opzioni (List[str], optional): Lista di 4 opzioni per domande multiple choice
        giustificazione (str, optional): Spiegazione della risposta per domande chiuse
    
    Note:
        - Per domande 'multipla': opzioni è obbligatorio, giustificazione consigliata
        - Per domande 'vero_falso': giustificazione è obbligatoria
        - Per domande 'aperta': opzioni e giustificazione non utilizzate
    
    Usage:
        # Domanda aperta
        flashcard = FlashcardData(
            domanda="Qual è la capitale d'Italia?",
            risposta="Roma",
            tipo="aperta",
            punteggio=2
        )
        
        # Domanda multiple choice
        flashcard = FlashcardData(
            domanda="Quale di questi è un pianeta?",
            risposta="Marte",
            tipo="multipla",
            punteggio=3,
            opzioni=["Marte", "Luna", "Sole", "Stella"],
            giustificazione="Marte è l'unico pianeta tra le opzioni..."
        )
    """
    domanda: str                        # La domanda formulata dall'IA
    risposta: str                       # La risposta corretta
    tipo: str                          # Tipo: 'aperta', 'vero_falso', 'multipla'
    punteggio: int                     # Difficoltà da 1 (facile) a 5 (difficile)
    opzioni: List[str] = None          # Opzioni per multiple choice (4 elementi)
    giustificazione: Optional[str] = None  # Spiegazione per domande chiuse

@dataclass
class PDFStatistics:
    """
    Statistiche di elaborazione di un documento PDF.
    
    Contiene informazioni aggregate sull'elaborazione di un documento,
    utilizzate per fornire feedback all'utente e per il monitoraggio
    delle performance del sistema.
    
    Attributes:
        pages_processed (int): Numero di pagine elaborate con successo
        total_words (int): Numero totale di parole estratte dal documento
        flashcards_generated (int): Numero di flashcard generate con successo
    
    Usage:
        stats = PDFStatistics(
            pages_processed=10,
            total_words=2500,
            flashcards_generated=15
        )
        
        # Calcolo di metriche derivate
        avg_words_per_page = stats.total_words / stats.pages_processed
        flashcards_per_page = stats.flashcards_generated / stats.pages_processed
    """
    pages_processed: int        # Numero di pagine elaborate con successo
    total_words: int           # Totale parole estratte dal documento
    flashcards_generated: int  # Numero di flashcard generate

@dataclass
class ProcessingProgress:
    """
    Informazioni sul progresso di elaborazione in tempo reale.
    
    Utilizzata per comunicare al frontend lo stato di avanzamento
    dell'elaborazione di un documento PDF, permettendo di mostrare
    una barra di progresso e informazioni dettagliate all'utente.
    
    Attributes:
        current_part (int): Parte attualmente in elaborazione (1-based)
        total_parts (int): Numero totale di parti da elaborare
        percentage (int): Percentuale di completamento (0-100)
    
    Usage:
        progress = ProcessingProgress(
            current_part=2,
            total_parts=5,
            percentage=40
        )
        
        # Verifica se l'elaborazione è completata
        is_complete = progress.current_part == progress.total_parts
        
        # Calcolo del progresso rimanente
        remaining_parts = progress.total_parts - progress.current_part
    """
    current_part: int   # Parte corrente in elaborazione (inizia da 1)
    total_parts: int    # Numero totale di parti da elaborare
    percentage: int     # Percentuale di completamento (0-100) 