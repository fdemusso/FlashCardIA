import React from 'react';
import { Flashcard } from '../../types';

interface NavigationButtonsProps {
  card: Flashcard;
  currentCard: number;
  totalCards: number;
  showAnswer: boolean;
  userAnswer: string;
  onPrevious: () => void;
  onNext: () => void;
  onToggleAnswer: () => void;
}

export const NavigationButtons: React.FC<NavigationButtonsProps> = ({
  card,
  currentCard,
  totalCards,
  showAnswer,
  userAnswer,
  onPrevious,
  onNext,
  onToggleAnswer
}) => {
  return (
    <div className="mt-6 flex justify-between items-center">
      <button
        className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg disabled:opacity-50 hover:bg-gray-300 transition-colors"
        onClick={onPrevious}
        disabled={currentCard === 0}
      >
        ← Precedente
      </button>
      
      {/* Pulsante centrale: diverso per ogni tipo */}
      {card.tipo === 'aperta' && (
        <button
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          onClick={onToggleAnswer}
        >
          {showAnswer ? 'Nascondi Risposta' : 'Mostra Risposta'}
        </button>
      )}
      
      {(card.tipo === 'vero_falso' || card.tipo === 'multipla') && (
        <button
          className="px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors disabled:opacity-50"
          onClick={onToggleAnswer}
          disabled={!userAnswer}
        >
          {showAnswer ? 'Nascondi Giustificazione' : 'Giustifica Risposta'}
        </button>
      )}
      
      <button
        className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg disabled:opacity-50 hover:bg-gray-300 transition-colors"
        onClick={onNext}
        disabled={currentCard === totalCards - 1}
      >
        Successiva →
      </button>
    </div>
  );
}; 