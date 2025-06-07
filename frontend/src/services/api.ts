import axios from 'axios';
import { Flashcard, Statistics } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export interface UploadResponse {
  flashcards: Flashcard[];
  statistics: Statistics;
}

export interface ProgressData {
  type: 'progress' | 'complete' | 'error';
  data: any;
}

export const uploadPDF = async (
  file: File,
  onUploadProgress?: (progress: number) => void,
  onGenerationProgress?: (progress: any) => void
): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 600000, // 10 minuti di timeout
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total && onUploadProgress) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onUploadProgress(percentCompleted);
      }
    },
    responseType: 'text'
  });

  // Processa la risposta streaming
  const lines = response.data.split('\n').filter((line: string) => line.trim());
  let result: UploadResponse | null = null;
  
  for (const line of lines) {
    try {
      const data: ProgressData = JSON.parse(line);
      
      if (data.type === 'progress' && onGenerationProgress) {
        onGenerationProgress(data.data);
      } else if (data.type === 'complete') {
        result = {
          flashcards: data.data.flashcards,
          statistics: data.data.statistics
        };
      } else if (data.type === 'error') {
        throw new Error(data.data);
      }
    } catch (e) {
      console.error('Errore nel parsing della risposta:', e);
      throw new Error('Errore nel formato della risposta dal server');
    }
  }

  if (!result) {
    throw new Error('Nessun risultato ricevuto dal server');
  }

  return result;
};

export const validateFile = (file: File): string | null => {
  // Verifica che sia un PDF
  if (!file.name.toLowerCase().endsWith('.pdf')) {
    return 'Seleziona solo file PDF';
  }
  
  // Verifica dimensione del file (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    return 'Il file PDF è troppo grande (max 10MB)';
  }
  
  return null;
}; 