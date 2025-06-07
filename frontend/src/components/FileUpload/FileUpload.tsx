import React from 'react';
import { FaFileUpload, FaSpinner } from 'react-icons/fa';
import { UploadState } from '../../types';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';

interface FileUploadProps {
  uploadState: UploadState;
  onFileChange: (file: File | null) => void;
  onUpload: () => void;
  onErrorDismiss?: () => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  uploadState,
  onFileChange,
  onUpload,
  onErrorDismiss
}) => {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileChange(e.target.files[0]);
    } else {
      onFileChange(null);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">
          Carica un file PDF
        </label>
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={uploadState.loading}
        />
        {uploadState.file && (
          <div className="mt-2 text-sm text-gray-600">
            File selezionato: {uploadState.file.name} ({(uploadState.file.size / 1024 / 1024).toFixed(2)} MB)
          </div>
        )}
      </div>
      
      {uploadState.error && (
        <ErrorMessage 
          message={uploadState.error} 
          onDismiss={onErrorDismiss}
        />
      )}
      
      {uploadState.loading && (
        <LoadingSpinner
          message={uploadState.loadingMessage}
          progress={uploadState.generationProgress?.percentage}
          showProgress={!!uploadState.generationProgress}
        />
      )}
      
      <button
        className={`w-full flex items-center justify-center px-4 py-3 bg-blue-500 text-white rounded-lg font-medium transition-colors ${
          uploadState.loading || !uploadState.file 
            ? 'opacity-50 cursor-not-allowed' 
            : 'hover:bg-blue-600'
        }`}
        onClick={onUpload}
        disabled={!uploadState.file || uploadState.loading}
      >
        {uploadState.loading ? (
          <>
            <FaSpinner className="animate-spin mr-2" />
            Elaborazione...
          </>
        ) : (
          <>
            <FaFileUpload className="mr-2" />
            Genera Flashcard
          </>
        )}
      </button>
    </div>
  );
}; 