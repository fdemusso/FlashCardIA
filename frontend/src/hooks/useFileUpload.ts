import { useState } from 'react';
import { uploadPDF, validateFile } from '../services/api';
import { UploadState, Flashcard, Statistics, GenerationProgress } from '../types';
import axios from 'axios';

export const useFileUpload = () => {
  const [uploadState, setUploadState] = useState<UploadState>({
    file: null,
    loading: false,
    error: null,
    loadingMessage: '',
    generationProgress: null
  });

  const setFile = (file: File | null) => {
    if (file) {
      const validationError = validateFile(file);
      if (validationError) {
        setUploadState(prev => ({ ...prev, error: validationError, file: null }));
        return;
      }
    }
    setUploadState(prev => ({ ...prev, file, error: null }));
  };

  const uploadFile = async (): Promise<{ flashcards: Flashcard[]; statistics: Statistics } | null> => {
    if (!uploadState.file) {
      setUploadState(prev => ({ ...prev, error: 'Seleziona un file PDF' }));
      return null;
    }

    setUploadState(prev => ({
      ...prev,
      loading: true,
      error: null,
      loadingMessage: 'Caricamento del PDF...',
      generationProgress: null
    }));

    try {
      setUploadState(prev => ({ ...prev, loadingMessage: 'Estrazione del testo dal PDF...' }));
      
      const result = await uploadPDF(
        uploadState.file,
        (progress) => {
          setUploadState(prev => ({ ...prev, loadingMessage: `Caricamento PDF: ${progress}%` }));
        },
        (progress: GenerationProgress) => {
          setUploadState(prev => ({
            ...prev,
            generationProgress: progress,
            loadingMessage: `Generazione delle flashcard: ${progress.percentage}% (Parte ${progress.current_part} di ${progress.total_parts})`
          }));
        }
      );

      setUploadState(prev => ({
        ...prev,
        loading: false,
        loadingMessage: '',
        generationProgress: null
      }));

      return result;
    } catch (error) {
      console.error('Errore durante il caricamento:', error);
      let errorMessage = 'Errore durante la generazione delle flashcard';
      
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          errorMessage = 'Timeout: L\'elaborazione del PDF e la generazione delle flashcard richiede più tempo del previsto. Per favore, riprova con un file più piccolo o attendi più a lungo.';
        } else {
          errorMessage = error.response?.data?.detail || 'Errore durante la generazione delle flashcard';
        }
      }

      setUploadState(prev => ({
        ...prev,
        loading: false,
        error: errorMessage,
        loadingMessage: '',
        generationProgress: null
      }));

      return null;
    }
  };

  const resetUpload = () => {
    setUploadState({
      file: null,
      loading: false,
      error: null,
      loadingMessage: '',
      generationProgress: null
    });
  };

  return {
    uploadState,
    setFile,
    uploadFile,
    resetUpload
  };
}; 