import React from 'react';

interface ErrorMessageProps {
  message: string;
  onDismiss?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onDismiss }) => {
  return (
    <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg border border-red-200 relative">
      {message}
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="absolute top-2 right-2 text-red-500 hover:text-red-700"
        >
          ✕
        </button>
      )}
    </div>
  );
}; 