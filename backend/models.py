from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class TextChunk:
    content: str
    page_number: int
    word_count: int

@dataclass
class FlashcardData:
    domanda: str
    risposta: str
    tipo: str
    punteggio: int
    opzioni: List[str] = None
    giustificazione: Optional[str] = None

@dataclass
class PDFStatistics:
    pages_processed: int
    total_words: int
    flashcards_generated: int

@dataclass
class ProcessingProgress:
    current_part: int
    total_parts: int
    percentage: int 