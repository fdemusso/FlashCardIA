import logging
from typing import List

# Configurazione logging
logging.basicConfig(level=logging.INFO)

# Configurazioni CORS
ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:3002"]

# Configurazioni IA
AI_MODEL_NAME = 'gemma3:4b-it-qat'
MAX_WORDS_PER_CHUNK = 800
MAX_FLASHCARDS_LIMIT = 20

# Configurazioni PDF
MIN_WORDS_FOR_PROCESSING = 50
MIN_TEXT_LENGTH_AFTER_CLEANING = 20
MIN_PAGE_CONTENT_LENGTH = 10

# Configurazioni flashcard
VALID_CARD_TYPES = ["multipla", "vero_falso", "aperta"]
DEFAULT_SCORE = 3
MIN_QUESTION_LENGTH = 5
MIN_ANSWER_LENGTH = 1
MULTIPLE_CHOICE_OPTIONS_COUNT = 4

# Configurazioni Ollama
OLLAMA_OPTIONS = {
    "temperature": 0.1,
    "num_predict": 1000
} 