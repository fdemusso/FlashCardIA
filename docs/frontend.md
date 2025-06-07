# 📱 Frontend Documentation

## 📋 Overview

The frontend is developed in React with TypeScript, providing a modern and responsive user interface for interaction with the flashcard generation system. It uses a modular architecture based on custom hooks to separate business logic from presentation.

## 🏗️ Architecture

### Design Principles

- **Separation of Responsibilities**: Business logic in custom hooks, UI in components
- **Type Safety**: TypeScript to prevent runtime errors
- **Reusable Components**: Modular design for ease of maintenance
- **Local State Management**: Using React hooks for state management
- **Responsive Design**: Tailwind CSS for adaptive interface

### File Structure

```
frontend/src/
├── App.tsx                    # Main component and orchestrator
├── index.tsx                  # Application entry point
├── index.css                  # Global styles and Tailwind configuration
├── components/                # Reusable React components
│   ├── FlashcardViewer/      # Flashcard visualization and navigation
│   ├── FileUpload/           # PDF upload management
│   ├── Statistics/           # Document statistics visualization
│   └── common/               # Shared components (errors, loading)
├── hooks/                    # Custom hooks for business logic
│   ├── useFlashcards.ts      # Flashcard state and navigation management
│   └── useFileUpload.ts      # File upload and API communication management
├── services/                 # Services for external communication
│   └── api.ts                # API client for backend
├── types/                    # TypeScript definitions
│   └── index.ts              # Shared interfaces and types
└── utils/                    # Utility and helper functions (empty)
```

## 📄 File-by-File Documentation

### 🚀 App.tsx - Main Component

**Purpose**: Main orchestrator of the application, manages flow between upload and flashcard visualization.

**Responsibilities**:
- Coordination between upload and visualization
- Global application state management
- Conditional routing based on state
- Reset and navigation event handling

**Hooks Used**:
- `useFileUpload`: For PDF upload management
- `useFlashcards`: For flashcard and navigation management

### 🎯 types/index.ts - TypeScript Definitions

**Purpose**: Centralizes all type definitions to ensure type safety.

**Main Interfaces**:

```typescript
// Flashcard structure
interface Flashcard {
  domanda: string;
  risposta: string;
  tipo: 'multipla' | 'vero_falso' | 'aperta';
  opzioni?: string[];
  punteggio: number;
  giustificazione?: string;
}

// Processing statistics
interface Statistics {
  pages_processed: number;
  total_words: number;
  flashcards_generated: number;
}

// Upload state
interface UploadState {
  file: File | null;
  loading: boolean;
  error: string | null;
  loadingMessage: string;
  generationProgress: GenerationProgress | null;
}

// Flashcard state
interface FlashcardState {
  flashcards: Flashcard[];
  statistics: Statistics | null;
  currentCard: number;
  showAnswer: boolean;
  userAnswer: string;
  score: number;
}
```

### 🔧 services/api.ts - API Client

**Purpose**: Handles communication with backend via REST APIs.

**Main Functions**:
- `uploadPDF()`: PDF file upload with streaming handling
- NDJSON event parsing for real-time progress
- Network error and timeout handling
- Type safety for API responses

### 🎣 hooks/useFileUpload.ts - Upload Hook

**Purpose**: Handles the entire file upload process and backend communication.

**Features**:
- PDF file selection and validation
- Upload with progress tracking
- NDJSON stream parsing from backend
- Loading and error state management
- State reset for new uploads

**Managed States**:
- Selected file
- Loading status
- Progress messages
- Upload errors
- Processing progress

### 🃏 hooks/useFlashcards.ts - Flashcard Hook

**Purpose**: Manages flashcard state and navigation logic.

**Features**:
- Flashcard navigation (forward/backward)
- User answer management
- Answer visibility toggle
- Score calculation
- State reset for new session

**Managed States**:
- Flashcard list
- Current flashcard index
- Answer visibility
- User answer
- Total score
- Document statistics

## 🧩 Detailed Components

### 📁 FileUpload/FileUpload.tsx

**Purpose**: Interface for PDF file selection and upload.

**Features**:
- Drag & drop for PDF files
- File type validation
- Progress bar during upload
- Dynamic status messages
- Error handling with dismissal

**Props**:
```typescript
interface FileUploadProps {
  uploadState: UploadState;
  onFileChange: (file: File | null) => void;
  onUpload: () => Promise<void>;
  onErrorDismiss: () => void;
}
```

### 🎴 FlashcardViewer/FlashcardViewer.tsx

**Purpose**: Main container for flashcard visualization.

**Responsibilities**:
- Flashcard component orchestration
- Responsive layout management
- Navigation coordination
- User event handling

### 🎴 FlashcardViewer/QuestionCard.tsx

**Purpose**: Displays question and handles user interaction.

**Features**:
- Question rendering by type (open, true/false, multiple)
- Dynamic input based on question type
- Answer validation
- Visual feedback for correctness
- Difficulty score management

**Question Types**:
- **Open**: Free text field
- **True/False**: Radio buttons
- **Multiple Choice**: Selectable option list

### 🎴 FlashcardViewer/AnswerSection.tsx

**Purpose**: Shows correct answer and explanation.

**Features**:
- Conditional display
- Answer correctness feedback
- Explanation for closed questions
- Differentiated styling by type

### 🎴 FlashcardViewer/NavigationButtons.tsx

**Purpose**: Navigation controls between flashcards.

**Features**:
- Forward/backward navigation
- Intelligent button disabling
- Position counter
- Session reset
- Visual status indicators

### 📊 Statistics/Statistics.tsx

**Purpose**: Displays document processing statistics.

**Metrics Shown**:
- Pages processed
- Total words extracted
- Flashcards generated
- Derived metrics (words per page, etc.)

### 🔧 common/ErrorMessage.tsx

**Purpose**: Reusable component for error messages.

**Features**:
- Consistent styling
- Optional dismissal
- Status icons
- Accessibility

### 🔧 common/LoadingSpinner.tsx

**Purpose**: Reusable loading indicator.

**Variants**:
- Simple spinner
- With custom message
- Configurable dimensions
- Smooth animations

## 🎨 Styling and Design

### Tailwind CSS

**Approach**: Utility-first CSS framework for rapid prototyping and consistent design.

**Advantages**:
- Predefined classes for spacing, colors, layout
- Built-in responsive design
- Automatic purging of unused CSS
- Customization through configuration

### Design System

**Colors**:
- Primary: Blue for main actions
- Secondary: Gray for texts and borders
- Success: Green for positive feedback
- Error: Red for errors and warnings
- Neutral: Grays for backgrounds and containers

**Typography**:
- Font system: Inter/system fonts
- Typographic scale: text-sm, text-base, text-lg, text-xl, etc.
- Weights: font-normal, font-medium, font-semibold, font-bold

**Spacing**:
- System based on 4px multiples
- Classes: p-2, p-4, p-6, m-2, m-4, etc.
- Gap for flexbox/grid: gap-2, gap-4, etc.

## 🔄 Data Flow

### Upload Flow

1. **File Selection**: User selects PDF via FileUpload
2. **Validation**: File type and size checking
3. **Upload**: File sent to backend with progress tracking
4. **Streaming**: Progress events received via NDJSON
5. **Completion**: Flashcards and statistics received
6. **Transition**: Switch to visualization mode

### Flashcard Flow

1. **Initialization**: First flashcard loading
2. **Interaction**: User enters answer
3. **Validation**: Answer correctness checking
4. **Feedback**: Correct answer display
5. **Navigation**: Move to next flashcard
6. **Completion**: Session end with score

## 🚦 Error Handling

### Error Types

1. **Upload Errors**:
   - Invalid file
   - File too large
   - Network errors

2. **Processing Errors**:
   - Backend unavailable
   - Processing timeout
   - Insufficient PDF content

3. **Navigation Errors**:
   - Inconsistent state
   - Missing data

### Recovery Strategies

- **Automatic retry** for temporary network errors
- **Graceful fallback** for non-critical features
- **Informative messages** to guide user
- **State reset** to start over

## 📱 Responsive Design

### Breakpoints

- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (md/lg)
- **Desktop**: > 1024px (xl)

### Adaptations

- **Layout**: Vertical stack on mobile, grid on desktop
- **Typography**: Scaled sizes for readability
- **Spacing**: Reduced padding/margin on mobile
- **Interactions**: Touch-friendly on mobile

## 🧪 Testing and Debug

### Debug Tools

- **React DevTools**: Component and state inspection
- **Browser DevTools**: Network, console, performance
- **TypeScript**: Compile-time type checking
- **ESLint**: Linting and best practices

### Testing Strategy

- **Unit Tests**: Utility functions and hooks
- **Component Tests**: Rendering and interactions
- **Integration Tests**: Complete flows
- **E2E Tests**: Real user scenarios

## 🚀 Performance

### Optimizations

- **Code Splitting**: Lazy loading components
- **Memoization**: React.memo for pure components
- **Bundle Optimization**: Tree shaking and minification
- **Image Optimization**: Modern formats and lazy loading

### Metrics

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🔧 Build and Deploy

### Development

```bash
npm start          # Start development server
npm run build      # Production build
npm test           # Run tests
npm run lint       # Code linting
```

### Production

- **Optimized build**: Minification and compression
- **Static hosting**: Compatible with Netlify, Vercel, etc.
- **Environment variables**: Configuration for different environments
- **Service worker**: Caching and offline support (optional) 