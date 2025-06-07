/**
 * Componente principale dell'applicazione Generatore di Flashcard IA.
 * 
 * Questo componente funge da orchestratore principale dell'applicazione,
 * gestendo il flusso tra le due modalità principali:
 * 1. Upload e elaborazione di file PDF
 * 2. Visualizzazione e navigazione delle flashcard generate
 * 
 * Responsabilità:
 * - Coordinamento tra i custom hooks per upload e flashcard
 * - Gestione del routing condizionale basato sullo stato
 * - Orchestrazione degli eventi di reset e transizione
 * - Layout principale e struttura dell'interfaccia
 * 
 * Architettura:
 * - Utilizza custom hooks per separare logica business da presentazione
 * - Rendering condizionale per le diverse fasi dell'applicazione
 * - Gestione centralizzata degli eventi cross-componente
 */

import React from 'react';
import { useFileUpload } from './hooks/useFileUpload';
import { useFlashcards } from './hooks/useFlashcards';
import { FileUpload } from './components/FileUpload/FileUpload';
import { Statistics } from './components/Statistics/Statistics';
import { FlashcardViewer } from './components/FlashcardViewer/FlashcardViewer';

const App: React.FC = () => {
  // Hook per gestione upload file PDF e comunicazione con backend
  const { uploadState, setFile, uploadFile, resetUpload } = useFileUpload();
  
  // Hook per gestione stato flashcard e logica di navigazione
  const {
    flashcardState,
    setFlashcards,
    nextCard,
    previousCard,
    setUserAnswer,
    toggleShowAnswer,
    setShowAnswer,
    resetFlashcards
  } = useFlashcards();

  /**
   * Gestisce il processo di upload del file PDF.
   * 
   * Coordina l'upload del file tramite il hook useFileUpload e,
   * in caso di successo, inizializza lo stato delle flashcard
   * con i dati ricevuti dal backend.
   * 
   * Flusso:
   * 1. Invoca l'upload tramite il hook
   * 2. Attende il completamento dell'elaborazione
   * 3. Se successo, imposta flashcard e statistiche
   * 4. Trigger automatico del cambio di modalità (rendering condizionale)
   */
  const handleUpload = async () => {
    const result = await uploadFile();
    if (result) {
      // Imposta le flashcard generate e le statistiche del documento
      setFlashcards(result.flashcards, result.statistics);
    }
  };

  /**
   * Gestisce il reset completo dell'applicazione.
   * 
   * Riporta l'applicazione allo stato iniziale, permettendo
   * all'utente di caricare un nuovo documento PDF.
   * Coordina il reset di entrambi gli hook per garantire
   * uno stato pulito.
   */
  const handleReset = () => {
    resetFlashcards();  // Reset stato flashcard e navigazione
    resetUpload();      // Reset stato upload e file selezionato
  };

  /**
   * Gestisce la dismissione degli errori di upload.
   * 
   * Placeholder per futura implementazione di logica
   * di gestione errori più sofisticata (es. retry automatico,
   * logging, analytics).
   */
  const handleErrorDismiss = () => {
    // Potresti implementare una logica per nascondere l'errore se necessario
    // Es: clearError() dal hook useFileUpload
  };

  return (
    // Container principale con layout responsive e styling Tailwind
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        {/* Header dell'applicazione */}
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Generatore di Flashcard IA
        </h1>

        {/* Rendering condizionale basato sulla presenza di flashcard */}
        {!flashcardState.flashcards.length ? (
          // Modalità Upload: Mostra interfaccia per caricamento PDF
          <FileUpload
            uploadState={uploadState}
            onFileChange={setFile}
            onUpload={handleUpload}
            onErrorDismiss={handleErrorDismiss}
          />
        ) : (
          // Modalità Flashcard: Mostra statistiche e viewer
          <div>
            {/* Statistiche del documento elaborato (se disponibili) */}
            {flashcardState.statistics && (
              <Statistics statistics={flashcardState.statistics} />
            )}
            
            {/* Viewer principale per navigazione flashcard */}
            <FlashcardViewer
              flashcardState={flashcardState}
              onNext={nextCard}
              onPrevious={previousCard}
              onAnswerChange={setUserAnswer}
              onToggleAnswer={toggleShowAnswer}
              onSetShowAnswer={setShowAnswer}
              onReset={handleReset}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default App; 