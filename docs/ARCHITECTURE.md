# Architecture Guide

## Overview

arvesha-research follows a clean architecture pattern with clear separation of concerns across all layers.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Frontend (Next.js 14)                  │
│  Pages → Components → Services (Axios) → Backend API        │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / SSE
┌──────────────────────────▼──────────────────────────────────┐
│                       Backend (FastAPI)                       │
│                                                              │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐ │
│  │   API   │→ │ Services │→ │  Repos   │→ │   Models    │ │
│  │ Routers │  │(Business)│  │(Data     │  │(SQLAlchemy) │ │
│  └─────────┘  └──────────┘  │ Access)  │  └─────────────┘ │
│                              └──────────┘                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                Core Layer                            │   │
│  │  Config | Database | Security | Logging | Middleware │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────┬───────────────┬──────────────┬──────────────┘
               │               │              │
        ┌──────▼──┐     ┌──────▼──┐    ┌─────▼───┐
        │PostgreSQL│     │  Redis  │    │ChromaDB │
        │(Primary) │     │(Cache)  │    │(Vector) │
        └─────────┘     └─────────┘    └─────────┘
```

## Backend Layers

### API Layer (`app/api/`)
HTTP route handlers. Validates input via Pydantic schemas, delegates to services, returns responses.

### Service Layer (`app/services/`)
Business logic. Orchestrates data access, external API calls, AI operations.

### Repository Layer (`app/repositories/`)
Data access abstraction. Generic `BaseRepository[T]` using async SQLAlchemy.

### Model Layer (`app/models/`)
SQLAlchemy ORM models: `User`, `ResearchExperiment`, `Dataset`, `Document`, `Message`, `Benchmark`.

### Core Layer (`app/core/`)
- `config.py` — Pydantic BaseSettings, reads from `.env`
- `database.py` — Lazy async engine, `get_db` dependency, `create_all_tables`
- `security.py` — JWT creation/verification, bcrypt password hashing, `get_current_user` dependency
- `logging.py` — structlog configuration (JSON structured logs)
- `middleware.py` — `RequestIDMiddleware` (X-Request-ID header), `LoggingMiddleware` (access logs)

## Frontend Architecture

```
src/
├── app/            # Next.js App Router pages (file-based routing)
├── components/     # Reusable React components
│   ├── layout/     # MainLayout, Sidebar
│   └── ui/         # Button, Card, Badge, Spinner
├── hooks/          # Custom hooks (useAuth)
├── services/       # API client functions (axios)
├── store/          # Zustand global state (auth)
├── types/          # TypeScript interfaces
└── lib/            # Utilities (cn helper)
```

### State Management
- **Zustand** with `persist` middleware for auth (token stored in localStorage)
- **SWR** for server state / data fetching with automatic revalidation

### API Communication
- `axios` instance in `src/services/api.ts`
- Request interceptor: injects `Authorization: Bearer <token>`
- Response interceptor: redirects to `/login` on 401

## AI Pipeline Architecture

### RAG Pipeline
```
User Query
    │
    ▼
Embed Query (SentenceTransformers all-MiniLM-L6-v2)
    │
    ▼
Vector Search (ChromaDB cosine similarity)
    │
    ▼
Rerank (cosine similarity reranking)
    │
    ▼
Build Context (top-k chunks concatenated)
    │
    ▼
LLM Generation (OpenAI-compatible API)
    │
    ▼
Response + Citations
```

### Agent Architecture
LangChain ReAct agents with tool use:
- **ResearchAgent**: `search_knowledge` tool
- **SummarizationAgent**: `summarize_text` tool
- **DataExtractionAgent**: `extract_data` tool

### Embedding Pipeline
```
File Upload → Parse (PDF/CSV/JSON/TXT) → Chunk (512 tokens, 50 overlap)
    → SentenceTransformer embed → ChromaDB store → PostgreSQL metadata
```

## Data Flow

### Authentication
```
POST /auth/register → hash password (bcrypt) → store User → return UserResponse
POST /auth/login    → verify password → create JWT → return TokenResponse
GET  any protected  → HTTPBearer → verify JWT → get User → inject into handler
```

### Experiment Lifecycle
```
POST /research/experiment     → create ResearchExperiment row
GET  /research/experiments    → list user's experiments
GET  /research/experiment/:id → fetch single experiment
DELETE /research/experiment/:id → delete experiment
```

## Technology Choices

| Component | Technology | Reason |
|-----------|-----------|--------|
| Web Framework | FastAPI | Async, automatic OpenAPI docs, Pydantic integration |
| ORM | SQLAlchemy 2.x async | Type-safe, async-first |
| Database | PostgreSQL | Production-grade, supports JSONB |
| Vector DB | ChromaDB | Easy self-hosting, good Python API |
| Embeddings | SentenceTransformers | Local, no API cost |
| AI Framework | LangChain | Standard agent framework |
| Cache | Redis | Fast key-value, session storage |
| Auth | JWT (python-jose) | Stateless, scalable |
| Frontend | Next.js 14 App Router | SSR, TypeScript, great DX |
| State | Zustand | Lightweight, persists to localStorage |
| Data Fetching | SWR | Stale-while-revalidate caching |
