"""
Configurazioni centrali per l'applicazione Generatore di Flashcard IA.

Questo modulo centralizza tutte le configurazioni dell'applicazione,
organizzate per categoria funzionale. Include:
- Configurazioni di rete e CORS
- Parametri per il modello di intelligenza artificiale
- Limiti e soglie per l'elaborazione PDF
- Validazioni e parametri per le flashcard
- Opzioni per il servizio Ollama

Tutte le configurazioni sono definite come costanti per facilitare
la manutenzione e permettere modifiche centralizzate.
"""

import logging
from typing import List

# ============================================================================
# CONFIGURAZIONE LOGGING
# ============================================================================

# Configurazione del sistema di logging per l'intera applicazione
# Livello INFO per tracciare operazioni normali e milestone importanti
logging.basicConfig(level=logging.INFO)

# ============================================================================
# CONFIGURAZIONI CORS E NETWORKING
# ============================================================================

# Domini autorizzati per le richieste CORS dal frontend
# Include le porte standard per sviluppo React (3000) e alternative (3002)
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:3002"]

# ============================================================================
# CONFIGURAZIONI INTELLIGENZA ARTIFICIALE
# ============================================================================

# Nome del modello Ollama da utilizzare per la generazione di flashcard
# gemma3:4b-it-qat è ottimizzato per l'italiano e ha buone performance
AI_MODEL_NAME = 'gemma3:4b-it-qat'

# Numero massimo di parole per chunk inviato all'IA
# Bilanciato per fornire contesto sufficiente senza superare i limiti del modello
MAX_WORDS_PER_CHUNK = 800

# Limite massimo di flashcard generate per documento
# Previene elaborazioni eccessive e mantiene tempi di risposta ragionevoli
MAX_FLASHCARDS_LIMIT = 20

# ============================================================================
# CONFIGURAZIONI ELABORAZIONE PDF
# ============================================================================

# Numero minimo di parole richieste per avviare l'elaborazione
# Documenti troppo corti non forniscono contenuto sufficiente per flashcard significative
MIN_WORDS_FOR_PROCESSING = 50

# Lunghezza minima del testo dopo la pulizia per considerare una pagina valida
# Filtra pagine con solo artefatti di formattazione o contenuto non testuale
MIN_TEXT_LENGTH_AFTER_CLEANING = 20

# Lunghezza minima del contenuto grezzo per considerare una pagina
# Prima verifica per scartare rapidamente pagine vuote o quasi vuote
MIN_PAGE_CONTENT_LENGTH = 10

# ============================================================================
# CONFIGURAZIONI VALIDAZIONE FLASHCARD
# ============================================================================

# Tipi di flashcard supportati dall'applicazione
# Ogni tipo ha logiche di validazione e presentazione specifiche
VALID_CARD_TYPES = ["multipla", "vero_falso", "aperta"]

# Punteggio di difficoltà di default (scala 1-5)
# Assegnato quando l'IA non fornisce un punteggio valido
DEFAULT_SCORE = 3

# Lunghezza minima per il testo della domanda
# Garantisce che le domande siano sufficientemente dettagliate
MIN_QUESTION_LENGTH = 5

# Lunghezza minima per il testo della risposta
# Permette risposte molto brevi (es. "Sì", "No") ma filtra risposte vuote
MIN_ANSWER_LENGTH = 1

# Numero di opzioni richieste per domande multiple choice
# Standard di 4 opzioni per bilanciare difficoltà e usabilità
MULTIPLE_CHOICE_OPTIONS_COUNT = 4

# ============================================================================
# CONFIGURAZIONI OLLAMA
# ============================================================================

# Opzioni di configurazione per le richieste al modello Ollama
OLLAMA_OPTIONS = {
    # Temperatura bassa per risposte più deterministiche e coerenti
    # Valori bassi (0.1) riducono la creatività ma aumentano la precisione
    "temperature": 0.1,
    
    # Limite massimo di token per la risposta del modello
    # Bilanciato per permettere risposte complete senza timeout
    "num_predict": 1000
} 