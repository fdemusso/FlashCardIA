"""
Processore per l'estrazione e l'elaborazione di testo da documenti PDF.

Questo modulo gestisce l'intero pipeline di elaborazione dei PDF:
- Estrazione del testo pagina per pagina usando PyPDF2
- Pulizia e normalizzazione del testo estratto
- Rimozione di elementi indesiderati (numeri di pagina, caratteri di controllo)
- Raggruppamento intelligente del testo in porzioni ottimali per l'IA
- Gestione robusta degli errori di lettura e parsing

Il processore è ottimizzato per:
- Documenti educativi e accademici
- Testi in italiano
- Compatibilità con il servizio IA Ollama
"""

import PyPDF2
import re
import logging
from typing import List
from fastapi import HTTPException

from models import TextChunk
from config import MIN_TEXT_LENGTH_AFTER_CLEANING, MIN_PAGE_CONTENT_LENGTH, MAX_WORDS_PER_CHUNK

# Configurazione del logger per tracciare le operazioni di elaborazione PDF
logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Pulisce il testo estratto dal PDF rimuovendo caratteri indesiderati e formattazioni problematiche.
    
    Questa funzione applica una serie di trasformazioni per migliorare la qualità
    del testo estratto dai PDF, che spesso contiene artefatti di formattazione,
    caratteri di controllo e elementi non testuali.
    
    Operazioni di pulizia:
    1. Rimozione caratteri di controllo e non stampabili
    2. Normalizzazione degli spazi bianchi
    3. Rimozione numeri di pagina isolati
    4. Eliminazione linee troppo corte (probabilmente artefatti)
    5. Ricomposizione delle parole spezzate
    6. Normalizzazione spazi multipli
    
    Args:
        text (str): Testo grezzo estratto dal PDF
    
    Returns:
        str: Testo pulito e normalizzato, pronto per l'elaborazione IA
        
    Note:
        La funzione è conservativa: preferisce mantenere testo dubbioso
        piuttosto che rimuovere contenuto potenzialmente valido.
    """
    if not text:
        return ""
    
    # Fase 1: Rimozione caratteri di controllo e sostituzione con spazi
    # I caratteri di controllo possono causare problemi nel parsing JSON
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', ' ', text)
    
    # Fase 2: Normalizzazione degli spazi bianchi
    # Converte tab, newline multipli e spazi multipli in spazi singoli
    text = re.sub(r'\s+', ' ', text)
    
    # Fase 3: Rimozione numeri di pagina isolati
    # Rimuove linee che contengono solo numeri (tipicamente numeri di pagina)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Fase 4: Filtraggio linee troppo corte
    # Rimuove linee con meno di 3 caratteri (probabilmente artefatti)
    lines = text.split('\n')
    lines = [line.strip() for line in lines if len(line.strip()) > 3]
    
    # Fase 5: Ricomposizione del testo
    # Unisce le linee valide con spazi per ricomporre il testo continuo
    text = ' '.join(lines)
    
    # Fase 6: Normalizzazione finale degli spazi
    # Rimuove spazi multipli che potrebbero essersi creati durante la pulizia
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

def extract_text_from_pdf(pdf_file) -> List[TextChunk]:
    """
    Estrae il testo dal PDF dividendolo per pagine e creando chunks gestibili.
    
    Questa funzione è il punto di ingresso principale per l'elaborazione PDF.
    Gestisce l'intero processo di estrazione, dalla lettura del file alla
    creazione di oggetti TextChunk strutturati.
    
    Processo di estrazione:
    1. Apertura e lettura del PDF con PyPDF2
    2. Iterazione su ogni pagina del documento
    3. Estrazione del testo grezzo da ogni pagina
    4. Applicazione della pulizia del testo
    5. Validazione della qualità del testo estratto
    6. Creazione di TextChunk con metadati
    
    Args:
        pdf_file: File-like object contenente il PDF da elaborare
    
    Returns:
        List[TextChunk]: Lista di chunk di testo, uno per ogni pagina valida
        
    Raises:
        HTTPException: Per errori di lettura del PDF o file corrotti
        
    Note:
        Le pagine con contenuto insufficiente vengono saltate ma loggiate.
        Il processo continua anche se alcune pagine falliscono.
    """
    chunks = []
    
    try:
        # Inizializzazione del reader PDF
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        logger.info(f"PDF con {len(pdf_reader.pages)} pagine caricato")
        
        # Elaborazione di ogni pagina del documento
        for page_num, page in enumerate(pdf_reader.pages, 1):
            try:
                # Estrazione del testo grezzo dalla pagina corrente
                raw_text = page.extract_text()
                
                # Controllo preliminare: verifica che ci sia contenuto
                if not raw_text or len(raw_text.strip()) < MIN_PAGE_CONTENT_LENGTH:
                    logger.warning(f"Pagina {page_num} contiene poco o nessun testo")
                    continue
                
                # Applicazione della pulizia del testo
                cleaned_text = clean_text(raw_text)
                
                # Controllo post-pulizia: verifica che rimanga contenuto sufficiente
                if len(cleaned_text) < MIN_TEXT_LENGTH_AFTER_CLEANING:
                    logger.warning(f"Pagina {page_num} contiene testo insufficiente dopo la pulizia")
                    continue
                
                # Calcolo delle statistiche del testo
                word_count = len(cleaned_text.split())
                
                logger.info(f"Pagina {page_num}: {word_count} parole estratte")
                
                # Creazione del TextChunk con metadati completi
                chunks.append(TextChunk(
                    content=cleaned_text,
                    page_number=page_num,
                    word_count=word_count
                ))
                
            except Exception as e:
                # Gestione errori per singola pagina (non blocca l'intero processo)
                logger.error(f"Errore nell'estrazione del testo dalla pagina {page_num}: {str(e)}")
                continue
        
        return chunks
        
    except Exception as e:
        # Gestione errori critici di lettura PDF
        logger.error(f"Errore nella lettura del PDF: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Errore nella lettura del PDF: {str(e)}")

def merge_chunks_intelligently(chunks: List[TextChunk], max_words: int = MAX_WORDS_PER_CHUNK) -> List[str]:
    """
    Unisce i chunks in modo intelligente per creare testi di dimensione ottimale per l'IA.
    
    Questa funzione raggruppa i TextChunk estratti dalle pagine in porzioni
    di dimensione ottimale per l'elaborazione da parte del modello IA.
    L'obiettivo è bilanciare:
    - Contesto sufficiente per domande significative
    - Dimensione gestibile per il modello IA
    - Coerenza tematica del contenuto
    
    Strategia di raggruppamento:
    1. Accumula chunk consecutivi fino al limite di parole
    2. Quando il limite viene raggiunto, inizia un nuovo gruppo
    3. Mantiene l'ordine originale delle pagine
    4. Aggiunge separatori tra pagine diverse
    
    Args:
        chunks (List[TextChunk]): Lista di chunk estratti dal PDF
        max_words (int): Numero massimo di parole per gruppo (default da config)
    
    Returns:
        List[str]: Lista di testi raggruppati, pronti per l'elaborazione IA
        
    Note:
        Se un singolo chunk supera il limite, viene comunque incluso
        per evitare perdita di contenuto.
    """
    if not chunks:
        return []
    
    merged_texts = []
    current_text = ""
    current_word_count = 0
    
    # Elaborazione di ogni chunk in sequenza
    for chunk in chunks:
        # Controllo se aggiungere questo chunk supererebbe il limite
        if current_word_count + chunk.word_count > max_words and current_text:
            # Salva il gruppo corrente e inizia un nuovo gruppo
            merged_texts.append(current_text.strip())
            current_text = chunk.content
            current_word_count = chunk.word_count
        else:
            # Aggiungi al gruppo corrente
            if current_text:
                # Separatore tra pagine diverse per mantenere struttura
                current_text += "\n\n" + chunk.content
            else:
                # Primo chunk del gruppo
                current_text = chunk.content
            current_word_count += chunk.word_count
    
    # Aggiungi l'ultimo gruppo se presente
    if current_text.strip():
        merged_texts.append(current_text.strip())
    
    logger.info(f"Testo diviso in {len(merged_texts)} parti per l'elaborazione")
    return merged_texts 