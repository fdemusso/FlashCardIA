export interface Flashcard {
  domanda: string;
  risposta: string;
  tipo: 'multipla' | 'vero_falso' | 'aperta';
  opzioni?: string[];
  punteggio: number;
  giustificazione?: string;
}

export interface Statistics {
  pages_processed: number;
  total_words: number;
  flashcards_generated: number;
}

export interface GenerationProgress {
  current_part: number;
  total_parts: number;
  percentage: number;
}

export interface UploadState {
  file: File | null;
  loading: boolean;
  error: string | null;
  loadingMessage: string;
  generationProgress: GenerationProgress | null;
}

export interface FlashcardState {
  flashcards: Flashcard[];
  statistics: Statistics | null;
  currentCard: number;
  showAnswer: boolean;
  userAnswer: string;
  score: number;
} 