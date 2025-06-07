/**
 * Definizioni TypeScript per l'applicazione Generatore di Flashcard IA.
 * 
 * Questo modulo centralizza tutte le interfacce e tipi utilizzati
 * nell'applicazione frontend, garantendo type safety e coerenza
 * dei dati tra componenti e servizi.
 * 
 * Organizzazione:
 * - Interfacce per entità business (Flashcard, Statistics)
 * - Interfacce per stati dell'applicazione (UploadState, FlashcardState)
 * - Tipi per comunicazione e progresso (GenerationProgress)
 * 
 * Benefici:
 * - Type checking compile-time
 * - IntelliSense e autocompletamento
 * - Documentazione implicita delle strutture dati
 * - Refactoring sicuro
 */

/**
 * Rappresenta una singola flashcard educativa.
 * 
 * Struttura dati principale per le flashcard generate dall'IA,
 * supporta tre tipi diversi di domande con campi specifici
 * per ogni tipologia.
 * 
 * Tipi supportati:
 * - 'multipla': Domande a scelta multipla con 4 opzioni
 * - 'vero_falso': Affermazioni da verificare come vere o false
 * - 'aperta': Domande che richiedono risposte libere
 */
export interface Flashcard {
  /** La domanda formulata dall'IA */
  domanda: string;
  
  /** La risposta corretta (formato varia per tipo) */
  risposta: string;
  
  /** Tipo di flashcard che determina il rendering e la validazione */
  tipo: 'multipla' | 'vero_falso' | 'aperta';
  
  /** 
   * Lista di opzioni per domande multiple choice.
   * Obbligatorio per tipo 'multipla', ignorato per altri tipi.
   * Deve contenere esattamente 4 elementi.
   */
  opzioni?: string[];
  
  /** 
   * Punteggio di difficoltà da 1 (facile) a 5 (difficile).
   * Utilizzato per feedback visivo e statistiche.
   */
  punteggio: number;
  
  /** 
   * Spiegazione della risposta corretta.
   * Obbligatorio per tipi 'multipla' e 'vero_falso',
   * non utilizzato per tipo 'aperta'.
   */
  giustificazione?: string;
}

/**
 * Statistiche di elaborazione di un documento PDF.
 * 
 * Contiene informazioni aggregate sull'elaborazione
 * di un documento, utilizzate per fornire feedback
 * all'utente sulla qualità e quantità del contenuto elaborato.
 */
export interface Statistics {
  /** Numero di pagine del PDF elaborate con successo */
  pages_processed: number;
  
  /** Numero totale di parole estratte dal documento */
  total_words: number;
  
  /** Numero di flashcard generate dall'IA */
  flashcards_generated: number;
}

/**
 * Informazioni sul progresso di elaborazione in tempo reale.
 * 
 * Utilizzata per comunicare lo stato di avanzamento
 * dell'elaborazione di un documento PDF, permettendo
 * di mostrare una progress bar e informazioni dettagliate.
 */
export interface GenerationProgress {
  /** Parte attualmente in elaborazione (1-based) */
  current_part: number;
  
  /** Numero totale di parti da elaborare */
  total_parts: number;
  
  /** Percentuale di completamento (0-100) */
  percentage: number;
}

/**
 * Stato dell'upload e elaborazione file PDF.
 * 
 * Gestisce tutto il ciclo di vita dell'upload:
 * dalla selezione del file al completamento dell'elaborazione,
 * includendo stati di loading, errori e progresso.
 */
export interface UploadState {
  /** File PDF selezionato dall'utente (null se nessun file) */
  file: File | null;
  
  /** Indica se è in corso un'operazione di upload/elaborazione */
  loading: boolean;
  
  /** Messaggio di errore (null se nessun errore) */
  error: string | null;
  
  /** Messaggio descrittivo dello stato corrente dell'elaborazione */
  loadingMessage: string;
  
  /** 
   * Informazioni dettagliate sul progresso dell'elaborazione.
   * null quando non è in corso un'elaborazione.
   */
  generationProgress: GenerationProgress | null;
}

/**
 * Stato delle flashcard e della sessione di studio.
 * 
 * Gestisce tutto lo stato relativo alla visualizzazione
 * e navigazione delle flashcard, inclusi i progressi
 * dell'utente e le statistiche della sessione.
 */
export interface FlashcardState {
  /** Lista delle flashcard generate (vuota inizialmente) */
  flashcards: Flashcard[];
  
  /** 
   * Statistiche del documento elaborato.
   * null quando non ci sono flashcard caricate.
   */
  statistics: Statistics | null;
  
  /** 
   * Indice della flashcard attualmente visualizzata (0-based).
   * -1 o 0 quando non ci sono flashcard.
   */
  currentCard: number;
  
  /** 
   * Indica se la risposta corretta è attualmente visibile.
   * Utilizzato per il toggle show/hide della risposta.
   */
  showAnswer: boolean;
  
  /** 
   * Risposta inserita dall'utente per la flashcard corrente.
   * Stringa vuota quando non è stata inserita alcuna risposta.
   */
  userAnswer: string;
  
  /** 
   * Punteggio totale accumulato durante la sessione.
   * Calcolato sommando i punteggi delle risposte corrette.
   */
  score: number;
} 