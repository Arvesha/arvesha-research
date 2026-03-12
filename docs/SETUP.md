# Setup Guide

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://python.org) |
| Node.js | 20+ | [nodejs.org](https://nodejs.org) |
| Docker | 24+ | [docker.com](https://docker.com) |
| PostgreSQL | 16 | Required for local dev without Docker |
| Redis | 7 | Required for local dev without Docker |

---

## Option 1: Docker Setup (Recommended)

### 1. Clone and configure
```bash
git clone https://github.com/Arvesha/arvesha-research.git
cd arvesha-research

cp .env.example .env
```

Edit `.env` and set at minimum:
```
OPENAI_API_KEY=sk-...
SECRET_KEY=a-very-long-random-string-at-least-32-chars
```

### 2. Start all services
```bash
docker compose up -d
```

This starts:
- **backend** on port 8000
- **frontend** on port 3000
- **postgres** on port 5432
- **redis** on port 6379
- **chromadb** on port 8001

### 3. Verify
```bash
curl http://localhost:8000/health
# {"status":"healthy","service":"arvesha-research-api","version":"1.0.0"}

open http://localhost:3000
```

### 4. View logs
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### 5. Stop
```bash
docker compose down
# To also remove volumes:
docker compose down -v
```

---

## Option 2: Local Development

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL, OPENAI_API_KEY, etc.

# Start PostgreSQL and Redis locally (or use Docker for just these services)
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine
docker run -d --name redis -p 6379:6379 redis:7-alpine
docker run -d --name chromadb -p 8001:8000 chromadb/chroma:latest

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API available at: http://localhost:8000  
Swagger UI: http://localhost:8000/docs  
ReDoc: http://localhost:8000/redoc

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local if backend is not on localhost:8000

# Run development server
npm run dev
```

Frontend available at: http://localhost:3000

---

## Running Tests

### Backend Tests
```bash
cd backend
source venv/bin/activate

# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

# Open coverage report
open htmlcov/index.html
```

Tests use SQLite in-memory — no PostgreSQL required.

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

---

## Environment Variables Reference

### Backend (`.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL async URL |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis URL |
| `SECRET_KEY` | Yes | dev key | JWT signing secret |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `1440` | Token expiry (24h) |
| `OPENAI_API_KEY` | Yes* | — | API key (*required for AI features) |
| `OPENAI_BASE_URL` | No | OpenAI default | OpenAI-compatible base URL |
| `DEFAULT_MODEL` | No | `gpt-4o-mini` | Default LLM model |
| `CHROMA_HOST` | No | `localhost` | ChromaDB host |
| `CHROMA_PORT` | No | `8001` | ChromaDB port |
| `EMBEDDING_MODEL` | No | `all-MiniLM-L6-v2` | SentenceTransformer model |

### Frontend (`.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL |

---

## Using an OpenAI-Compatible API

The platform works with any OpenAI-compatible provider (Ollama, LM Studio, Together, Groq, etc.):

```env
# Example: Ollama local
OPENAI_API_KEY=ollama
OPENAI_BASE_URL=http://localhost:11434/v1
DEFAULT_MODEL=llama3.2

# Example: Groq
OPENAI_API_KEY=gsk_...
OPENAI_BASE_URL=https://api.groq.com/openai/v1
DEFAULT_MODEL=llama-3.1-70b-versatile
```

---

## Production Deployment

For production:
1. Set `SECRET_KEY` to a strong random value (e.g., `openssl rand -hex 32`)
2. Set `POSTGRES_PASSWORD` to a strong password
3. Use environment-specific `.env` files
4. Configure proper CORS origins in `backend/app/main.py`
5. Set up TLS termination (nginx/traefik in front of Docker)
6. Use external managed PostgreSQL/Redis for durability
