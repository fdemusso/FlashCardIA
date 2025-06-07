# 📱 Documentazione Frontend

## 📋 Panoramica

Il frontend è sviluppato in React con TypeScript, fornisce un'interfaccia utente moderna e responsive per l'interazione con il sistema di generazione flashcard. Utilizza un'architettura modulare basata su custom hooks per separare la logica business dalla presentazione.

## 🏗️ Architettura

### Principi di Design

- **Separazione delle Responsabilità**: Logica business nei custom hooks, UI nei componenti
- **Type Safety**: TypeScript per prevenire errori runtime
- **Componenti Riutilizzabili**: Design modulare per facilità di manutenzione
- **State Management Locale**: Utilizzo di React hooks per gestione stato
- **Responsive Design**: Tailwind CSS per interfaccia adattiva

### Struttura dei File

```
frontend/src/
├── App.tsx                    # Componente principale e orchestratore
├── index.tsx                  # Entry point dell'applicazione
├── index.css                  # Stili globali e configurazione Tailwind
├── components/                # Componenti React riutilizzabili
│   ├── FlashcardViewer/      # Visualizzazione e navigazione flashcard
│   ├── FileUpload/           # Gestione upload PDF
│   ├── Statistics/           # Visualizzazione statistiche documento
│   └── common/               # Componenti condivisi (errori, loading)
├── hooks/                    # Custom hooks per logica business
│   ├── useFlashcards.ts      # Gestione stato flashcard e navigazione
│   └── useFileUpload.ts      # Gestione upload file e comunicazione API
├── services/                 # Servizi per comunicazione esterna
│   └── api.ts                # Client API per backend
├── types/                    # Definizioni TypeScript
│   └── index.ts              # Interfacce e tipi condivisi
└── utils/                    # Utility e helper functions (vuoto)
```

## 📄 Documentazione File per File

### 🚀 App.tsx - Componente Principale

**Scopo**: Orchestratore principale dell'applicazione, gestisce il flusso tra upload e visualizzazione flashcard.

**Responsabilità**:
- Coordinamento tra upload e visualizzazione
- Gestione dello stato globale dell'applicazione
- Routing condizionale basato sullo stato
- Gestione degli eventi di reset e navigazione

**Hook Utilizzati**:
- `useFileUpload`: Per gestione upload PDF
- `useFlashcards`: Per gestione flashcard e navigazione

### 🎯 types/index.ts - Definizioni TypeScript

**Scopo**: Centralizza tutte le definizioni di tipi per garantire type safety.

**Interfacce Principali**:

```typescript
// Struttura di una flashcard
interface Flashcard {
  domanda: string;
  risposta: string;
  tipo: 'multipla' | 'vero_falso' | 'aperta';
  opzioni?: string[];
  punteggio: number;
  giustificazione?: string;
}

// Statistiche di elaborazione
interface Statistics {
  pages_processed: number;
  total_words: number;
  flashcards_generated: number;
}

// Stato dell'upload
interface UploadState {
  file: File | null;
  loading: boolean;
  error: string | null;
  loadingMessage: string;
  generationProgress: GenerationProgress | null;
}

// Stato delle flashcard
interface FlashcardState {
  flashcards: Flashcard[];
  statistics: Statistics | null;
  currentCard: number;
  showAnswer: boolean;
  userAnswer: string;
  score: number;
}
```

### 🔧 services/api.ts - Client API

**Scopo**: Gestisce la comunicazione con il backend tramite API REST.

**Funzioni Principali**:
- `uploadPDF()`: Upload file PDF con gestione streaming
- Parsing eventi NDJSON per progresso real-time
- Gestione errori di rete e timeout
- Type safety per risposte API

### 🎣 hooks/useFileUpload.ts - Hook Upload

**Scopo**: Gestisce tutto il processo di upload file e comunicazione con backend.

**Funzionalità**:
- Selezione e validazione file PDF
- Upload con progress tracking
- Parsing stream NDJSON dal backend
- Gestione stati di loading ed errori
- Reset dello stato per nuovi upload

**Stati Gestiti**:
- File selezionato
- Stato di caricamento
- Messaggi di progresso
- Errori di upload
- Progresso elaborazione

### 🃏 hooks/useFlashcards.ts - Hook Flashcard

**Scopo**: Gestisce lo stato delle flashcard e la logica di navigazione.

**Funzionalità**:
- Navigazione tra flashcard (avanti/indietro)
- Gestione risposte utente
- Toggle visualizzazione risposta
- Calcolo punteggio
- Reset stato per nuova sessione

**Stati Gestiti**:
- Lista flashcard
- Indice flashcard corrente
- Visibilità risposta
- Risposta utente
- Punteggio totale
- Statistiche documento

## 🧩 Componenti Dettagliati

### 📁 FileUpload/FileUpload.tsx

**Scopo**: Interfaccia per selezione e upload file PDF.

**Caratteristiche**:
- Drag & drop per file PDF
- Validazione tipo file
- Progress bar durante upload
- Messaggi di stato dinamici
- Gestione errori con dismissal

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

**Scopo**: Container principale per visualizzazione flashcard.

**Responsabilità**:
- Orchestrazione componenti flashcard
- Gestione layout responsive
- Coordinamento navigazione
- Gestione eventi utente

### 🎴 FlashcardViewer/QuestionCard.tsx

**Scopo**: Visualizza la domanda e gestisce l'interazione utente.

**Funzionalità**:
- Rendering domande per tipo (aperta, vero/falso, multipla)
- Input dinamico basato su tipo domanda
- Validazione risposte
- Feedback visivo per correttezza
- Gestione punteggio difficoltà

**Tipi di Domande**:
- **Aperte**: Campo di testo libero
- **Vero/Falso**: Radio buttons
- **Multiple Choice**: Lista opzioni selezionabili

### 🎴 FlashcardViewer/AnswerSection.tsx

**Scopo**: Mostra la risposta corretta e la giustificazione.

**Caratteristiche**:
- Visualizzazione condizionale
- Feedback correttezza risposta
- Giustificazione per domande chiuse
- Styling differenziato per tipo

### 🎴 FlashcardViewer/NavigationButtons.tsx

**Scopo**: Controlli di navigazione tra flashcard.

**Funzionalità**:
- Navigazione avanti/indietro
- Disabilitazione intelligente bottoni
- Contatore posizione
- Reset sessione
- Indicatori visivi stato

### 📊 Statistics/Statistics.tsx

**Scopo**: Visualizza statistiche di elaborazione documento.

**Metriche Mostrate**:
- Pagine elaborate
- Parole totali estratte
- Flashcard generate
- Metriche derivate (parole per pagina, etc.)

### 🔧 common/ErrorMessage.tsx

**Scopo**: Componente riutilizzabile per messaggi di errore.

**Caratteristiche**:
- Styling consistente
- Dismissal opzionale
- Icone di stato
- Accessibilità

### 🔧 common/LoadingSpinner.tsx

**Scopo**: Indicatore di caricamento riutilizzabile.

**Varianti**:
- Spinner semplice
- Con messaggio personalizzato
- Dimensioni configurabili
- Animazioni smooth

## 🎨 Styling e Design

### Tailwind CSS

**Approccio**: Utility-first CSS framework per rapid prototyping e design consistente.

**Vantaggi**:
- Classi predefinite per spacing, colori, layout
- Responsive design built-in
- Purging automatico CSS non utilizzato
- Customizzazione tramite configurazione

### Design System

**Colori**:
- Primario: Blu per azioni principali
- Secondario: Grigio per testi e bordi
- Successo: Verde per feedback positivo
- Errore: Rosso per errori e warning
- Neutro: Grigi per background e contenitori

**Typography**:
- Font system: Inter/system fonts
- Scale tipografica: text-sm, text-base, text-lg, text-xl, etc.
- Pesi: font-normal, font-medium, font-semibold, font-bold

**Spacing**:
- Sistema basato su multipli di 4px
- Classi: p-2, p-4, p-6, m-2, m-4, etc.
- Gap per flexbox/grid: gap-2, gap-4, etc.

## 🔄 Flusso di Dati

### Upload Flow

1. **Selezione File**: Utente seleziona PDF tramite FileUpload
2. **Validazione**: Controllo tipo file e dimensioni
3. **Upload**: Invio file al backend con progress tracking
4. **Streaming**: Ricezione eventi progresso via NDJSON
5. **Completamento**: Ricezione flashcard e statistiche
6. **Transizione**: Passaggio a modalità visualizzazione

### Flashcard Flow

1. **Inizializzazione**: Caricamento prima flashcard
2. **Interazione**: Utente inserisce risposta
3. **Validazione**: Controllo correttezza risposta
4. **Feedback**: Visualizzazione risposta corretta
5. **Navigazione**: Passaggio alla flashcard successiva
6. **Completamento**: Fine sessione con punteggio

## 🚦 Gestione Errori

### Tipologie di Errori

1. **Errori di Upload**:
   - File non valido
   - Dimensioni eccessive
   - Errori di rete

2. **Errori di Elaborazione**:
   - Backend non disponibile
   - Timeout elaborazione
   - Contenuto PDF insufficiente

3. **Errori di Navigazione**:
   - Stato inconsistente
   - Dati mancanti

### Strategie di Recovery

- **Retry automatico** per errori di rete temporanei
- **Fallback graceful** per funzionalità non critiche
- **Messaggi informativi** per guidare l'utente
- **Reset stato** per ripartire da capo

## 📱 Responsive Design

### Breakpoints

- **Mobile**: < 640px (sm)
- **Tablet**: 640px - 1024px (md/lg)
- **Desktop**: > 1024px (xl)

### Adattamenti

- **Layout**: Stack verticale su mobile, grid su desktop
- **Typography**: Dimensioni scalate per leggibilità
- **Spacing**: Padding/margin ridotti su mobile
- **Interazioni**: Touch-friendly su mobile

## 🧪 Testing e Debug

### Strumenti di Debug

- **React DevTools**: Ispezione componenti e stato
- **Browser DevTools**: Network, console, performance
- **TypeScript**: Type checking compile-time
- **ESLint**: Linting e best practices

### Testing Strategy

- **Unit Tests**: Funzioni utility e hooks
- **Component Tests**: Rendering e interazioni
- **Integration Tests**: Flussi completi
- **E2E Tests**: Scenari utente reali

## 🚀 Performance

### Ottimizzazioni

- **Code Splitting**: Lazy loading componenti
- **Memoization**: React.memo per componenti puri
- **Bundle Optimization**: Tree shaking e minification
- **Image Optimization**: Formati moderni e lazy loading

### Metriche

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🔧 Build e Deploy

### Development

```bash
npm start          # Avvio development server
npm run build      # Build produzione
npm test           # Esecuzione test
npm run lint       # Linting codice
```

### Production

- **Build ottimizzato**: Minification e compression
- **Static hosting**: Compatibile con Netlify, Vercel, etc.
- **Environment variables**: Configurazione per diversi ambienti
- **Service worker**: Caching e offline support (opzionale) 