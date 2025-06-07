import PyPDF2
import re
import logging
from typing import List
from fastapi import HTTPException

from models import TextChunk
from config import MIN_TEXT_LENGTH_AFTER_CLEANING, MIN_PAGE_CONTENT_LENGTH, MAX_WORDS_PER_CHUNK

logger = logging.getLogger(__name__)

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
                
                if not raw_text or len(raw_text.strip()) < MIN_PAGE_CONTENT_LENGTH:
                    logger.warning(f"Pagina {page_num} contiene poco o nessun testo")
                    continue
                
                # Pulisci il testo
                cleaned_text = clean_text(raw_text)
                
                if len(cleaned_text) < MIN_TEXT_LENGTH_AFTER_CLEANING:
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

def merge_chunks_intelligently(chunks: List[TextChunk], max_words: int = MAX_WORDS_PER_CHUNK) -> List[str]:
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