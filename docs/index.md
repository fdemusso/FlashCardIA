# 📚 Indice Documentazione - Generatore di Flashcard IA

Benvenuto nella documentazione completa del progetto **Generatore di Flashcard IA**! Questa raccolta di documenti fornisce tutto il necessario per comprendere, utilizzare, sviluppare e deployare l'applicazione.

## 🗂️ Struttura della Documentazione

### 📖 Documentazione Generale

| Documento | Descrizione | Destinatari |
|-----------|-------------|-------------|
| **[README.md](../README.md)** | Panoramica del progetto e quick start | Tutti gli utenti |
| **[CHANGELOG.md](../CHANGELOG.md)** | Cronologia delle versioni e modifiche | Sviluppatori, utenti |

### 🏗️ Documentazione Tecnica

| Documento | Descrizione | Destinatari |
|-----------|-------------|-------------|
| **[Backend](./backend.md)** | Documentazione completa del backend Python/FastAPI | Sviluppatori backend |
| **[Frontend](./frontend.md)** | Documentazione completa del frontend React/TypeScript | Sviluppatori frontend |
| **[API](./api.md)** | Documentazione delle API REST | Sviluppatori, integratori |

### 🚀 Deployment e Operazioni

| Documento | Descrizione | Destinatari |
|-----------|-------------|-------------|
| **[Deployment](./deployment.md)** | Guida completa al deployment | DevOps, amministratori |
| **[Testing](./testing.md)** | Guide per test e debugging | Sviluppatori, QA |

## 🎯 Percorsi di Lettura Consigliati

### 👨‍💻 Per Sviluppatori Nuovi al Progetto

1. **[README.md](../README.md)** - Comprendi il progetto e fai il setup iniziale
2. **[Backend](./backend.md)** - Studia l'architettura del backend
3. **[Frontend](./frontend.md)** - Comprendi la struttura del frontend
4. **[API](./api.md)** - Familiarizza con le API
5. **[Testing](./testing.md)** - Impara a testare il codice

### 🚀 Per DevOps e Deployment

1. **[README.md](../README.md)** - Panoramica generale
2. **[Deployment](./deployment.md)** - Setup completo per produzione
3. **[API](./api.md)** - Comprendi gli endpoint per monitoring
4. **[Backend](./backend.md)** - Configurazioni e dipendenze

### 🔧 Per Integratori e API Users

1. **[API](./api.md)** - Documentazione completa delle API
2. **[Backend](./backend.md)** - Comprendi la logica di business
3. **[Testing](./testing.md)** - Test di integrazione

### 📱 Per Frontend Developers

1. **[Frontend](./frontend.md)** - Architettura e componenti
2. **[API](./api.md)** - Integrazione con backend
3. **[Testing](./testing.md)** - Test frontend

## 🔍 Ricerca Rapida

### 🚨 Risoluzione Problemi

| Problema | Dove Cercare |
|----------|--------------|
| **Ollama non funziona** | [Deployment - Troubleshooting](./deployment.md#troubleshooting) |
| **Errori API** | [API - Gestione Errori](./api.md#gestione-errori) |
| **Build fallisce** | [Deployment - Setup](./deployment.md#setup-ambiente-locale) |
| **Test non passano** | [Testing](./testing.md) |
| **Performance lente** | [Backend - Monitoring](./backend.md#monitoring) |

### ⚙️ Configurazioni

| Configurazione | Documento | Sezione |
|----------------|-----------|---------|
| **Variabili ambiente** | [Deployment](./deployment.md) | Configurazione Ambiente |
| **CORS** | [Backend](./backend.md) | Configurazioni |
| **Ollama** | [Deployment](./deployment.md) | Setup Ollama |
| **Docker** | [Deployment](./deployment.md) | Docker |
| **Nginx** | [Deployment](./deployment.md) | Reverse Proxy |

### 🧩 Componenti e Architettura

| Componente | Documento | Dettagli |
|------------|-----------|----------|
| **FastAPI Routes** | [Backend](./backend.md) | main.py |
| **React Components** | [Frontend](./frontend.md) | Componenti |
| **Custom Hooks** | [Frontend](./frontend.md) | Hooks |
| **IA Service** | [Backend](./backend.md) | ai_service.py |
| **PDF Processing** | [Backend](./backend.md) | pdf_processor.py |

## 📊 Metriche della Documentazione

- **Pagine totali**: 6
- **Linee di codice documentate**: 100%
- **Esempi di codice**: 50+
- **Diagrammi**: 2
- **Guide step-by-step**: 15+

## 🤝 Come Contribuire alla Documentazione

### Aggiornamento Documentazione

1. **Modifica i file Markdown** nella cartella `docs/`
2. **Mantieni la struttura** esistente
3. **Aggiungi esempi pratici** quando possibile
4. **Testa le procedure** descritte
5. **Aggiorna questo indice** se necessario

### Standard di Scrittura

- **Linguaggio**: Italiano
- **Tono**: Professionale ma accessibile
- **Formato**: Markdown con emoji per sezioni
- **Esempi**: Sempre funzionanti e testati
- **Link**: Relativi quando possibile

### Template per Nuove Sezioni

```markdown
# 🎯 Titolo Sezione

## 📋 Panoramica
Breve descrizione della sezione...

## 🔧 Implementazione
Dettagli tecnici...

## 💡 Esempi
Esempi pratici...

## 🚨 Troubleshooting
Problemi comuni e soluzioni...
```

## 📞 Supporto

Per domande sulla documentazione:

1. **Controlla** prima questo indice
2. **Cerca** nella sezione appropriata
3. **Consulta** il troubleshooting
4. **Apri** un issue su GitHub se necessario

## 🔄 Aggiornamenti

Questa documentazione viene aggiornata ad ogni release. Controlla il [CHANGELOG.md](../CHANGELOG.md) per le modifiche più recenti.

---

**Ultima modifica**: Dicembre 2024  
**Versione documentazione**: 1.0  
**Compatibile con**: Versione applicazione 3.0+ 