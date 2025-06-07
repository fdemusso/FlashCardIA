import { useState } from 'react';
import { FlashcardState, Flashcard, Statistics } from '../types';

export const useFlashcards = () => {
  const [flashcardState, setFlashcardState] = useState<FlashcardState>({
    flashcards: [],
    statistics: null,
    currentCard: 0,
    showAnswer: false,
    userAnswer: '',
    score: 0
  });

  const setFlashcards = (flashcards: Flashcard[], statistics: Statistics) => {
    setFlashcardState({
      flashcards,
      statistics,
      currentCard: 0,
      showAnswer: false,
      userAnswer: '',
      score: 0
    });
  };

  const nextCard = () => {
    if (flashcardState.currentCard < flashcardState.flashcards.length - 1) {
      setFlashcardState(prev => ({
        ...prev,
        currentCard: prev.currentCard + 1,
        showAnswer: false,
        userAnswer: ''
      }));
    }
  };

  const previousCard = () => {
    if (flashcardState.currentCard > 0) {
      setFlashcardState(prev => ({
        ...prev,
        currentCard: prev.currentCard - 1,
        showAnswer: false,
        userAnswer: ''
      }));
    }
  };

  const setUserAnswer = (answer: string) => {
    setFlashcardState(prev => ({ ...prev, userAnswer: answer }));
  };

  const toggleShowAnswer = () => {
    setFlashcardState(prev => ({ ...prev, showAnswer: !prev.showAnswer }));
  };

  const setShowAnswer = (show: boolean) => {
    setFlashcardState(prev => ({ ...prev, showAnswer: show }));
  };

  const resetFlashcards = () => {
    setFlashcardState({
      flashcards: [],
      statistics: null,
      currentCard: 0,
      showAnswer: false,
      userAnswer: '',
      score: 0
    });
  };

  const getCurrentCard = (): Flashcard | null => {
    if (flashcardState.flashcards.length === 0) return null;
    return flashcardState.flashcards[flashcardState.currentCard] || null;
  };

  return {
    flashcardState,
    setFlashcards,
    nextCard,
    previousCard,
    setUserAnswer,
    toggleShowAnswer,
    setShowAnswer,
    resetFlashcards,
    getCurrentCard
  };
}; 