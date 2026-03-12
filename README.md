# arvesha-research

> **AI Research Platform by Arvesha Intelligence**

A production-grade full-stack AI research platform for experimenting with LLM architectures, testing RAG pipelines, evaluating AI agents, and benchmarking models.

**Founder:** Arvind Sisodiya  
**Organization:** Arvesha Intelligence

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      arvesha-research                             │
├─────────────────────────┬────────────────────────────────────────┤
│  Frontend (Next.js 14)  │         Backend (FastAPI)               │
│  Port: 3000             │         Port: 8000                      │
│                         │                                         │
│  /dashboard             │  /api/v1/auth                           │
│  /experiments     ◄─────┼──► /api/v1/research                    │
│  /datasets              │  /api/v1/datasets                       │
│  /prompt-lab            │  /api/v1/rag                            │
│  /agents                │  /api/v1/agents                         │
│  /benchmarks            │  /api/v1/benchmark                      │
│                         │                                         │
│                         │  PostgreSQL + Redis + ChromaDB          │
└─────────────────────────┴────────────────────────────────────────┘
```

## 🚀 Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/Arvesha/arvesha-research.git
cd arvesha-research
cp .env.example .env
# Edit .env — set OPENAI_API_KEY and SECRET_KEY
docker compose up -d
open http://localhost:3000
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## 📚 Features

| Feature | Description |
|---------|-------------|
| 🔬 Research Workspace | Create & manage AI research experiments |
| 🧪 Prompt Lab | Test prompts with token/latency metrics |
| 📊 Dataset Manager | Upload JSON/CSV/TXT/PDF → auto-embed → vector store |
| 🔍 RAG Pipeline | Semantic search + rerank + LLM with citations + streaming |
| 🤖 Agent Playground | ResearchAgent, SummarizationAgent, DataExtractionAgent |
| 📈 Benchmarks | Compare models on latency, tokens, cost |

## 🧪 Testing

```bash
# Backend
cd backend && pytest tests/ -v --cov=app

# Frontend
cd frontend && npm test
```

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Setup Guide](docs/SETUP.md)
- [API Reference](docs/API.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch and open a Pull Request

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Built with ❤️ by [Arvesha Intelligence](https://arvesha.ai)
