import React from 'react';
import { FaCheckCircle } from 'react-icons/fa';
import { Flashcard } from '../../types';
import { AnswerSection } from './AnswerSection';
import { NavigationButtons } from './NavigationButtons';

interface QuestionCardProps {
  card: Flashcard;
  userAnswer: string;
  showAnswer: boolean;
  currentCard: number;
  totalCards: number;
  onAnswerChange: (answer: string) => void;
  onAnswerSubmit: () => void;
  onPrevious: () => void;
  onNext: () => void;
  onToggleAnswer: () => void;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  card,
  userAnswer,
  showAnswer,
  currentCard,
  totalCards,
  onAnswerChange,
  onAnswerSubmit,
  onPrevious,
  onNext,
  onToggleAnswer
}) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      <div className="mb-4">
        <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded">
          {card.tipo.replace('_', ' ')}
        </span>
        <span className="ml-2 bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded">
          Difficoltà: {card.punteggio}/5
        </span>
      </div>
      
      <h2 className="text-xl font-bold mb-4">{card.domanda}</h2>
      
      {/* Domande a scelta multipla */}
      {card.tipo === 'multipla' && card.opzioni && (
        <div className="space-y-2">
          {card.opzioni.map((opzione, index) => (
            <button
              key={index}
              className={`w-full text-left p-3 rounded border transition-colors ${
                userAnswer === opzione 
                  ? opzione === card.risposta
                    ? 'bg-green-100 border-green-300 text-green-800'
                    : 'bg-red-100 border-red-300 text-red-800'
                  : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
              }`}
              onClick={() => {
                onAnswerChange(opzione);
                onAnswerSubmit();
              }}
              disabled={showAnswer}
            >
              <span className="font-medium mr-2">{String.fromCharCode(65 + index)}.</span>
              {opzione}
            </button>
          ))}
        </div>
      )}

      {/* Domande vero/falso */}
      {card.tipo === 'vero_falso' && (
        <div className="flex space-x-4">
          <button
            className={`flex-1 px-6 py-3 rounded border transition-colors ${
              userAnswer === 'vero' 
                ? userAnswer === card.risposta
                  ? 'bg-green-100 border-green-300 text-green-800'
                  : 'bg-red-100 border-red-300 text-red-800'
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
            }`}
            onClick={() => {
              onAnswerChange('vero');
              onAnswerSubmit();
            }}
            disabled={showAnswer}
          >
            <FaCheckCircle className="inline mr-2" />
            Vero
          </button>
          <button
            className={`flex-1 px-6 py-3 rounded border transition-colors ${
              userAnswer === 'falso' 
                ? userAnswer === card.risposta
                  ? 'bg-green-100 border-green-300 text-green-800'
                  : 'bg-red-100 border-red-300 text-red-800'
                : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
            }`}
            onClick={() => {
              onAnswerChange('falso');
              onAnswerSubmit();
            }}
            disabled={showAnswer}
          >
            ✗ Falso
          </button>
        </div>
      )}

      {/* Domande aperte */}
      {card.tipo === 'aperta' && (
        <textarea
          className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={userAnswer}
          onChange={(e) => onAnswerChange(e.target.value)}
          placeholder="Scrivi la tua risposta..."
          rows={4}
        />
      )}

      {/* Sezione risposte - ora all'interno del riquadro */}
      <AnswerSection 
        card={card} 
        showAnswer={showAnswer} 
      />

      {/* Pulsanti di navigazione - ora all'interno del riquadro */}
      <NavigationButtons
        card={card}
        currentCard={currentCard}
        totalCards={totalCards}
        showAnswer={showAnswer}
        userAnswer={userAnswer}
        onPrevious={onPrevious}
        onNext={onNext}
        onToggleAnswer={onToggleAnswer}
      />
    </div>
  );
}; 