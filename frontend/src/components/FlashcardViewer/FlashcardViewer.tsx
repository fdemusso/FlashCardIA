import React from 'react';
import { FlashcardState } from '../../types';
import { QuestionCard } from './QuestionCard';
import { AnswerSection } from './AnswerSection';
import { NavigationButtons } from './NavigationButtons';

interface FlashcardViewerProps {
  flashcardState: FlashcardState;
  onNext: () => void;
  onPrevious: () => void;
  onAnswerChange: (answer: string) => void;
  onToggleAnswer: () => void;
  onSetShowAnswer: (show: boolean) => void;
  onReset: () => void;
}

export const FlashcardViewer: React.FC<FlashcardViewerProps> = ({
  flashcardState,
  onNext,
  onPrevious,
  onAnswerChange,
  onToggleAnswer,
  onSetShowAnswer,
  onReset
}) => {
  const { flashcards, currentCard, showAnswer, userAnswer } = flashcardState;
  const card = flashcards[currentCard];

  if (!card) return null;

  const handleAnswerSubmit = () => {
    onSetShowAnswer(true);
  };

  return (
    <div>
      <div className="text-center mb-6">
        <div className="inline-flex items-center bg-white rounded-lg shadow px-4 py-2">
          <span className="text-gray-600 mr-2">Flashcard</span>
          <span className="font-bold text-blue-600">{currentCard + 1}</span>
          <span className="text-gray-600 mx-1">di</span>
          <span className="font-bold text-blue-600">{flashcards.length}</span>
        </div>
        
        <button
          onClick={onReset}
          className="ml-4 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          Nuovo PDF
        </button>
      </div>
      
      <QuestionCard
        card={card}
        userAnswer={userAnswer}
        showAnswer={showAnswer}
        onAnswerChange={onAnswerChange}
        onAnswerSubmit={handleAnswerSubmit}
      />
      
      <AnswerSection 
        card={card} 
        showAnswer={showAnswer} 
      />
      
      <NavigationButtons
        card={card}
        currentCard={currentCard}
        totalCards={flashcards.length}
        showAnswer={showAnswer}
        userAnswer={userAnswer}
        onPrevious={onPrevious}
        onNext={onNext}
        onToggleAnswer={onToggleAnswer}
      />
    </div>
  );
}; 