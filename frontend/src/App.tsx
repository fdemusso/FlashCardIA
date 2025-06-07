import React from 'react';
import { useFileUpload } from './hooks/useFileUpload';
import { useFlashcards } from './hooks/useFlashcards';
import { FileUpload } from './components/FileUpload/FileUpload';
import { Statistics } from './components/Statistics/Statistics';
import { FlashcardViewer } from './components/FlashcardViewer/FlashcardViewer';

const App: React.FC = () => {
  const { uploadState, setFile, uploadFile, resetUpload } = useFileUpload();
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

  const handleUpload = async () => {
    const result = await uploadFile();
    if (result) {
      setFlashcards(result.flashcards, result.statistics);
    }
  };

  const handleReset = () => {
    resetFlashcards();
    resetUpload();
  };

  const handleErrorDismiss = () => {
    // Potresti implementare una logica per nascondere l'errore se necessario
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Generatore di Flashcard IA
        </h1>

        {!flashcardState.flashcards.length ? (
          <FileUpload
            uploadState={uploadState}
            onFileChange={setFile}
            onUpload={handleUpload}
            onErrorDismiss={handleErrorDismiss}
          />
        ) : (
          <div>
            {flashcardState.statistics && (
              <Statistics statistics={flashcardState.statistics} />
            )}
            
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