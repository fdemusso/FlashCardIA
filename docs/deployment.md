# 🚀 Guida al Deployment

## 📋 Panoramica

Questa guida copre il deployment completo dell'applicazione Generatore di Flashcard IA, dalla configurazione locale allo sviluppo fino al deployment in produzione.

## 🛠️ Prerequisiti di Sistema

### Software Richiesto

| Software | Versione Minima | Scopo |
|----------|----------------|-------|
| **Python** | 3.8+ | Backend FastAPI |
| **Node.js** | 16+ | Frontend React |
| **npm** | 8+ | Package manager frontend |
| **Ollama** | Latest | Servizio IA locale |
| **Git** | 2.0+ | Version control |

### Hardware Raccomandato

#### Sviluppo Locale
- **RAM**: 8GB minimo, 16GB raccomandato
- **Storage**: 10GB liberi (modelli IA occupano spazio)
- **CPU**: 4 core, supporto AVX per performance IA

#### Produzione
- **RAM**: 16GB minimo, 32GB raccomandato
- **Storage**: 50GB+ SSD
- **CPU**: 8+ core, GPU opzionale per IA
- **Network**: Banda stabile per upload PDF

## 🏠 Setup Ambiente Locale

### 1. Clone del Repository

```bash
# Clone del progetto
git clone <repository-url>
cd IA-flashcard

# Verifica struttura
ls -la
```

### 2. Setup Ollama

```bash
# Installazione Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Scarica da https://ollama.ai/download

# Avvio servizio
ollama serve

# Download modello (in un nuovo terminale)
ollama pull gemma3:4b-it-qat

# Verifica installazione
ollama list
```

### 3. Setup Backend

```bash
# Navigazione alla cartella backend
cd backend

# Creazione ambiente virtuale
python -m venv venv

# Attivazione ambiente virtuale
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Installazione dipendenze
pip install -r requirements.txt

# Verifica installazione
python -c "import fastapi, ollama, PyPDF2; print('Dipendenze OK')"

# Test avvio backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Setup Frontend

```bash
# Navigazione alla cartella frontend (nuovo terminale)
cd frontend

# Installazione dipendenze
npm install

# Verifica installazione
npm list --depth=0

# Test avvio frontend
npm start
```

### 5. Verifica Setup Completo

```bash
# Test health check backend
curl http://localhost:8000/health

# Verifica frontend
# Apri http://localhost:3000 nel browser

# Test upload (con file PDF di prova)
curl -X POST -F "file=@test.pdf" http://localhost:8000/upload-pdf
```

## 🔧 Configurazione Ambiente

### Variabili d'Ambiente

#### Backend (.env)

```bash
# Crea file backend/.env
cat > backend/.env << EOF
# Configurazione Ollama
OLLAMA_HOST=http://localhost:11434
AI_MODEL_NAME=gemma3:4b-it-qat

# Configurazione CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3002

# Configurazione logging
LOG_LEVEL=INFO

# Configurazione limiti
MAX_FILE_SIZE=10485760  # 10MB
MAX_FLASHCARDS=20
EOF
```

#### Frontend (.env)

```bash
# Crea file frontend/.env
cat > frontend/.env << EOF
# URL del backend
REACT_APP_API_URL=http://localhost:8000

# Configurazione build
GENERATE_SOURCEMAP=false
EOF
```

### Configurazione Ollama

```bash
# File di configurazione Ollama (~/.ollama/config.json)
mkdir -p ~/.ollama
cat > ~/.ollama/config.json << EOF
{
  "host": "0.0.0.0:11434",
  "models_path": "~/.ollama/models",
  "keep_alive": "5m",
  "max_concurrent_requests": 4
}
EOF
```

## 🐳 Deployment con Docker

### Dockerfile Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installazione dipendenze sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia codice applicazione
COPY . .

# Espone porta
EXPOSE 8000

# Comando di avvio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copia package files
COPY package*.json ./
RUN npm ci --only=production

# Copia codice e build
COPY . .
RUN npm run build

# Stage produzione
FROM nginx:alpine

# Copia build
COPY --from=builder /app/build /usr/share/nginx/html

# Configurazione nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    restart: unless-stopped

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - AI_MODEL_NAME=gemma3:4b-it-qat
    depends_on:
      - ollama
    restart: unless-stopped
    volumes:
      - ./backend:/app
      - /app/__pycache__

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  ollama_data:
```

### Comandi Docker

```bash
# Build e avvio completo
docker-compose up --build

# Avvio in background
docker-compose up -d

# Download modello Ollama
docker-compose exec ollama ollama pull gemma3:4b-it-qat

# Logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop
docker-compose down

# Cleanup completo
docker-compose down -v --rmi all
```

## ☁️ Deployment Cloud

### AWS EC2

#### 1. Preparazione Istanza

```bash
# Connessione EC2
ssh -i key.pem ubuntu@ec2-instance-ip

# Update sistema
sudo apt update && sudo apt upgrade -y

# Installazione Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Installazione Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Deploy Applicazione

```bash
# Clone repository
git clone <repository-url>
cd IA-flashcard

# Configurazione produzione
cp docker-compose.yml docker-compose.prod.yml

# Modifica per produzione
sed -i 's/localhost:8000/your-domain.com/g' docker-compose.prod.yml

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Setup modello IA
docker-compose exec ollama ollama pull gemma3:4b-it-qat
```

#### 3. Configurazione Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/flashcard-app
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Upload size limit
    client_max_body_size 10M;
}
```

```bash
# Attivazione configurazione
sudo ln -s /etc/nginx/sites-available/flashcard-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Vercel (Frontend Only)

```bash
# Installazione Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel

# Configurazione environment variables
vercel env add REACT_APP_API_URL production
# Inserire: https://your-backend-domain.com
```

### Railway/Render (Backend)

```yaml
# railway.toml o render.yaml
[build]
  builder = "DOCKERFILE"
  dockerfilePath = "backend/Dockerfile"

[deploy]
  startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
  healthcheckPath = "/health"

[env]
  OLLAMA_HOST = "https://your-ollama-service.com"
  AI_MODEL_NAME = "gemma3:4b-it-qat"
```

## 🔒 Configurazione Sicurezza

### SSL/TLS con Let's Encrypt

```bash
# Installazione Certbot
sudo apt install certbot python3-certbot-nginx

# Ottenimento certificato
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Aggiungi: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall

```bash
# UFW setup
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Verifica
sudo ufw status
```

### Environment Variables Sicure

```bash
# Usa secrets manager per produzione
# AWS Secrets Manager, Azure Key Vault, etc.

# Per Docker, usa secrets
echo "your-secret-key" | docker secret create api_key -
```

## 📊 Monitoring e Logging

### Logging Centralizzato

```yaml
# docker-compose.yml - aggiunta logging
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Health Checks

```bash
# Script di monitoring
#!/bin/bash
# health-check.sh

BACKEND_URL="http://localhost:8000/health"
FRONTEND_URL="http://localhost:3000"

# Check backend
if curl -f $BACKEND_URL > /dev/null 2>&1; then
    echo "Backend: OK"
else
    echo "Backend: FAIL"
    # Restart service
    docker-compose restart backend
fi

# Check frontend
if curl -f $FRONTEND_URL > /dev/null 2>&1; then
    echo "Frontend: OK"
else
    echo "Frontend: FAIL"
    docker-compose restart frontend
fi
```

### Metriche con Prometheus

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flashcard-backend'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest
      
      - name: Test Frontend
        run: |
          cd frontend
          npm ci
          npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /path/to/app
            git pull origin main
            docker-compose down
            docker-compose up -d --build
```

## 🚨 Troubleshooting

### Problemi Comuni

#### Ollama non risponde
```bash
# Verifica servizio
sudo systemctl status ollama

# Restart
sudo systemctl restart ollama

# Logs
journalctl -u ollama -f
```

#### Errori di memoria
```bash
# Monitoring memoria
free -h
docker stats

# Cleanup Docker
docker system prune -a
```

#### Timeout upload
```bash
# Aumenta timeout nginx
proxy_read_timeout 600s;
proxy_send_timeout 600s;

# Aumenta timeout FastAPI
uvicorn main:app --timeout-keep-alive 600
```

### Backup e Recovery

```bash
# Backup modelli Ollama
tar -czf ollama-backup.tar.gz ~/.ollama/models

# Backup configurazioni
tar -czf config-backup.tar.gz backend/.env frontend/.env

# Recovery
tar -xzf ollama-backup.tar.gz -C ~/
tar -xzf config-backup.tar.gz
```

## 📈 Scaling

### Load Balancing

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### Database per Sessioni

```python
# Per scaling orizzontale, considera Redis per sessioni
import redis

redis_client = redis.Redis(host='redis-server', port=6379, db=0)
```

Questa documentazione fornisce una guida completa per il deployment dell'applicazione in diversi ambienti, dalla configurazione locale al deployment in produzione con considerazioni per sicurezza, monitoring e scaling. 