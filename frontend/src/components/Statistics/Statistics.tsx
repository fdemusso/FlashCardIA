import React from 'react';
import { FaInfoCircle } from 'react-icons/fa';
import { Statistics as StatisticsType } from '../../types';

interface StatisticsProps {
  statistics: StatisticsType;
}

export const Statistics: React.FC<StatisticsProps> = ({ statistics }) => {
  return (
    <div className="bg-blue-50 rounded-lg p-4 mb-6 max-w-2xl mx-auto">
      <div className="flex items-center mb-2">
        <FaInfoCircle className="text-blue-500 mr-2" />
        <h3 className="font-semibold text-blue-800">Statistiche del documento</h3>
      </div>
      <div className="grid grid-cols-3 gap-4 text-sm">
        <div className="text-center">
          <div className="font-bold text-blue-600">{statistics.pages_processed}</div>
          <div className="text-blue-700">Pagine elaborate</div>
        </div>
        <div className="text-center">
          <div className="font-bold text-blue-600">{statistics.total_words}</div>
          <div className="text-blue-700">Parole totali</div>
        </div>
        <div className="text-center">
          <div className="font-bold text-blue-600">{statistics.flashcards_generated}</div>
          <div className="text-blue-700">Flashcard generate</div>
        </div>
      </div>
    </div>
  );
}; 