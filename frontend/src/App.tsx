import React, { useState } from 'react';
import axios from 'axios';
import { FaFileUpload, FaSpinner, FaCheckCircle, FaInfoCircle } from 'react-icons/fa';

interface Flashcard {
  domanda: string;
  risposta: string;
  tipo: 'multipla' | 'vero_falso' | 'aperta';
  opzioni?: string[];
  punteggio: number;
}

interface Statistics {
  pages_processed: number;
  total_words: number;
  flashcards_generated: number;
}

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [currentCard, setCurrentCard] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [userAnswer, setUserAnswer] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [score, setScore] = useState(0);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [generationProgress, setGenerationProgress] = useState<{
    current_part: number;
    total_parts: number;
    percentage: number;
  } | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      
      // Verifica che sia un PDF
      if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
        setError('Seleziona solo file PDF');
        return;
      }
      
      // Verifica dimensione del file (max 10MB)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('Il file PDF è troppo grande (max 10MB)');
        return;
      }
      
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Seleziona un file PDF');
      return;
    }

    setLoading(true);
    setError(null);
    setLoadingMessage('Caricamento del PDF...');
    setGenerationProgress(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoadingMessage('Estrazione del testo dal PDF...');
      
      const response = await axios.post('http://localhost:8000/upload-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 600000, // 10 minuti di timeout
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setLoadingMessage(`Caricamento PDF: ${percentCompleted}%`);
          }
        },
        responseType: 'stream'
      });

      setLoadingMessage('Generazione delle flashcard in corso...');
      
      // Leggi lo stream di risposta
      const reader = response.data.getReader();
      let result = '';
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        // Converti il chunk in stringa
        const chunk = new TextDecoder().decode(value);
        result += chunk;
        
        // Processa ogni oggetto JSON nel chunk
        const lines = result.split('\n');
        result = lines.pop() || ''; // Mantieni l'ultima linea incompleta
        
        for (const line of lines) {
          if (line.trim()) {
            try {
              const data = JSON.parse(line);
              if (data.type === 'progress') {
                setGenerationProgress(data.data);
                setLoadingMessage(`Generazione delle flashcard: ${data.data.percentage}% (Parte ${data.data.current_part} di ${data.data.total_parts})`);
              } else if (data.type === 'complete') {
                setFlashcards(data.data.flashcards);
                setStatistics(data.data.statistics);
                setCurrentCard(0);
                setShowAnswer(false);
                setScore(0);
                setLoadingMessage('');
                setGenerationProgress(null);
              }
            } catch (e) {
              console.error('Errore nel parsing della risposta:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Errore durante il caricamento:', error);
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNABORTED') {
          setError('Timeout: L\'elaborazione del PDF e la generazione delle flashcard richiede più tempo del previsto. Per favore, riprova con un file più piccolo o attendi più a lungo.');
        } else {
          setError(error.response?.data?.detail || 'Errore durante la generazione delle flashcard');
        }
      } else {
        setError('Errore durante la generazione delle flashcard');
      }
    } finally {
      setLoading(false);
      setLoadingMessage('');
      setGenerationProgress(null);
    }
  };

  const handleNext = () => {
    if (currentCard < flashcards.length - 1) {
      setCurrentCard(currentCard + 1);
      setShowAnswer(false);
      setUserAnswer('');
    }
  };

  const handlePrevious = () => {
    if (currentCard > 0) {
      setCurrentCard(currentCard - 1);
      setShowAnswer(false);
      setUserAnswer('');
    }
  };

  const handleReset = () => {
    setFlashcards([]);
    setStatistics(null);
    setFile(null);
    setCurrentCard(0);
    setShowAnswer(false);
    setUserAnswer('');
    setError(null);
    setScore(0);
  };

  const renderStatistics = () => {
    if (!statistics) return null;

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

  const renderQuestion = () => {
    const card = flashcards[currentCard];
    if (!card) return null;

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
                  setUserAnswer(opzione);
                  setShowAnswer(true);
                }}
                disabled={showAnswer}
              >
                <span className="font-medium mr-2">{String.fromCharCode(65 + index)}.</span>
                {opzione}
              </button>
            ))}
          </div>
        )}

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
                setUserAnswer('vero');
                setShowAnswer(true);
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
                setUserAnswer('falso');
                setShowAnswer(true);
              }}
              disabled={showAnswer}
            >
              ✗ Falso
            </button>
          </div>
        )}

        {card.tipo === 'aperta' && (
          <textarea
            className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={userAnswer}
            onChange={(e) => setUserAnswer(e.target.value)}
            placeholder="Scrivi la tua risposta..."
            rows={4}
          />
        )}

        {showAnswer && card.tipo === 'aperta' && (
          <div className="mt-6 p-4 bg-gray-50 rounded-lg border-l-4 border-blue-500">
            <h3 className="font-bold text-gray-800 mb-2">Risposta corretta:</h3>
            <p className="text-gray-700">{card.risposta}</p>
          </div>
        )}

        <div className="mt-6 flex justify-between items-center">
          <button
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg disabled:opacity-50 hover:bg-gray-300 transition-colors"
            onClick={handlePrevious}
            disabled={currentCard === 0}
          >
            ← Precedente
          </button>
          
          <button
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            onClick={() => setShowAnswer(!showAnswer)}
          >
            {showAnswer ? 'Nascondi Risposta' : 'Mostra Risposta'}
          </button>
          
          <button
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg disabled:opacity-50 hover:bg-gray-300 transition-colors"
            onClick={handleNext}
            disabled={currentCard === flashcards.length - 1}
          >
            Successiva →
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Generatore di Flashcard IA
        </h1>

        {!flashcards.length ? (
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
                disabled={loading}
              />
              {file && (
                <div className="mt-2 text-sm text-gray-600">
                  File selezionato: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </div>
              )}
            </div>
            
            {error && (
              <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg border border-red-200">
                {error}
              </div>
            )}
            
            {loading && (
              <div className="mb-4 p-3 bg-blue-100 text-blue-700 rounded-lg border border-blue-200">
                <div className="flex items-center">
                  <FaSpinner className="animate-spin mr-2" />
                  {loadingMessage || 'Elaborazione in corso...'}
                </div>
              </div>
            )}
            
            <button
              className={`w-full flex items-center justify-center px-4 py-3 bg-blue-500 text-white rounded-lg font-medium transition-colors ${
                loading || !file 
                  ? 'opacity-50 cursor-not-allowed' 
                  : 'hover:bg-blue-600'
              }`}
              onClick={handleUpload}
              disabled={!file || loading}
            >
              {loading ? (
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
        ) : (
          <div>
            {renderStatistics()}
            
            <div className="text-center mb-6">
              <div className="inline-flex items-center bg-white rounded-lg shadow px-4 py-2">
                <span className="text-gray-600 mr-2">Flashcard</span>
                <span className="font-bold text-blue-600">{currentCard + 1}</span>
                <span className="text-gray-600 mx-1">di</span>
                <span className="font-bold text-blue-600">{flashcards.length}</span>
              </div>
              
              <button
                onClick={handleReset}
                className="ml-4 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Nuovo PDF
              </button>
            </div>
            
            {renderQuestion()}
          </div>
        )}
      </div>
    </div>
  );
};

export default App; 