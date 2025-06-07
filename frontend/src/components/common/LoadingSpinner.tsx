import React from 'react';
import { FaSpinner } from 'react-icons/fa';

interface LoadingSpinnerProps {
  message?: string;
  progress?: number;
  showProgress?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
  message = 'Elaborazione in corso...', 
  progress, 
  showProgress = false 
}) => {
  return (
    <div className="mb-4 p-3 bg-blue-100 text-blue-700 rounded-lg border border-blue-200">
      <div className="flex items-center">
        <FaSpinner className="animate-spin mr-2" />
        {message}
      </div>
      {showProgress && progress !== undefined && (
        <div className="mt-2">
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="text-sm mt-1 text-center">
            {progress}% completato
          </div>
        </div>
      )}
    </div>
  );
}; 