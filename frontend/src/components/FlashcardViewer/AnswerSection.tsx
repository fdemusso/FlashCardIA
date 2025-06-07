import React from 'react';
import { Flashcard } from '../../types';

interface AnswerSectionProps {
  card: Flashcard;
  showAnswer: boolean;
}

export const AnswerSection: React.FC<AnswerSectionProps> = ({ card, showAnswer }) => {
  if (!showAnswer) return null;

  return (
    <>
      {/* Visualizzazione risposte aperte */}
      {card.tipo === 'aperta' && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border-l-4 border-blue-500">
          <h3 className="font-bold text-gray-800 mb-2">Risposta corretta:</h3>
          <p className="text-gray-700">{card.risposta}</p>
        </div>
      )}

      {/* Visualizzazione giustificazioni per vero/falso e multipla */}
      {(card.tipo === 'vero_falso' || card.tipo === 'multipla') && card.giustificazione && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          <h3 className="font-bold text-blue-800 mb-2">Giustificazione:</h3>
          <p className="text-blue-700">{card.giustificazione}</p>
          {card.tipo === 'multipla' && (
            <div className="mt-3 p-3 bg-green-100 rounded-lg">
              <p className="text-green-800 font-medium">
                <span className="font-bold">Risposta corretta:</span> {card.risposta}
              </p>
            </div>
          )}
        </div>
      )}
    </>
  );
}; 