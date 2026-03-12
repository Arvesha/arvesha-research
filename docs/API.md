# API Reference

Base URL: `http://localhost:8000/api/v1`

All protected endpoints require `Authorization: Bearer <token>` header.

Interactive docs: http://localhost:8000/docs

---

## Authentication

### POST /auth/register
Register a new user.

**Request:**
```json
{
  "username": "researcher",
  "email": "researcher@example.com",
  "password": "securepassword"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "researcher",
  "email": "researcher@example.com",
  "is_active": true
}
```

---

### POST /auth/login
Login and get JWT token.

**Request:**
```json
{
  "username": "researcher",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## Research Workspace

### POST /research/experiment 🔒
Create a new research experiment.

**Request:**
```json
{
  "title": "RAG Evaluation with GPT-4",
  "description": "Testing RAG pipeline accuracy",
  "dataset": "arxiv-papers",
  "model": "gpt-4o-mini",
  "prompt_template": "You are a research assistant. Answer based on context."
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "RAG Evaluation with GPT-4",
  "description": "Testing RAG pipeline accuracy",
  "dataset": "arxiv-papers",
  "model": "gpt-4o-mini",
  "prompt_template": "You are a research assistant...",
  "created_at": "2024-01-01T12:00:00Z",
  "user_id": 1
}
```

---

### GET /research/experiments 🔒
List all experiments for the current user.

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "RAG Evaluation",
    "model": "gpt-4o-mini",
    "created_at": "2024-01-01T12:00:00Z",
    "user_id": 1
  }
]
```

---

### GET /research/experiment/{id} 🔒
Get a single experiment by ID.

---

### DELETE /research/experiment/{id} 🔒
Delete an experiment.

**Response: 204 No Content**

---

### POST /research/test-prompt 🔒
Test a prompt against a model.

**Request:**
```json
{
  "prompt": "Explain the transformer architecture",
  "model": "gpt-4o-mini",
  "temperature": 0.7
}
```

**Response (200):**
```json
{
  "response": "The transformer architecture consists of...",
  "tokens_used": 250,
  "latency_ms": 1243.5
}
```

---

## Dataset Manager

### POST /datasets/upload 🔒
Upload a dataset file (multipart/form-data).

**Form fields:**
- `file`: file (JSON, CSV, TXT, or PDF)
- `description`: string (optional)

**Response (201):**
```json
{
  "id": 1,
  "name": "research-papers.pdf",
  "file_type": "pdf",
  "chunks_count": 47,
  "message": "Dataset uploaded successfully"
}
```

---

### GET /datasets/ 🔒
List all datasets for the current user.

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "research-papers.pdf",
    "file_type": "pdf",
    "chunks_count": 47,
    "created_at": "2024-01-01T12:00:00Z",
    "user_id": 1
  }
]
```

---

### DELETE /datasets/{id} 🔒
Delete a dataset.

**Response: 204 No Content**

---

## RAG Pipeline

### POST /rag/query 🔒
Run a RAG query.

**Request:**
```json
{
  "query": "What are the key findings of the paper?",
  "dataset_id": 1,
  "top_k": 5,
  "use_rerank": true,
  "stream": false
}
```

**Response (200) — non-streaming:**
```json
{
  "answer": "The key findings include...",
  "sources": [
    {
      "content": "In this paper, we present...",
      "document_id": "abc123",
      "score": 0.87,
      "metadata": {"dataset_id": 1, "chunk_index": 3}
    }
  ],
  "tokens_used": 430,
  "latency_ms": 2100.3
}
```

**Response (200) — streaming (`stream: true`):**

Server-Sent Events stream:
```
data: The key
data: findings
data: include...
data: [DONE]
```

---

## Agent Playground

### POST /agents/run 🔒
Run an AI agent.

**Agent types:** `research` | `summarization` | `data_extraction`

**Request:**
```json
{
  "agent_type": "research",
  "input": "Summarize the latest advances in transformer architectures",
  "tools": []
}
```

**Response (200):**
```json
{
  "output": "Recent advances in transformer architectures include...",
  "steps": [
    {
      "step": 1,
      "action": "search_knowledge",
      "observation": "Found relevant information about transformers"
    }
  ],
  "tokens_used": 320,
  "agent_type": "research"
}
```

---

## Benchmark System

### POST /benchmark/run 🔒
Run a model benchmark.

**Request:**
```json
{
  "name": "GPT-4 vs GPT-3.5 Comparison",
  "models": ["gpt-4o-mini", "gpt-3.5-turbo"],
  "prompts": [
    "What is machine learning?",
    "Explain attention mechanisms"
  ],
  "metrics": ["latency", "tokens", "cost"]
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "GPT-4 vs GPT-3.5 Comparison",
  "results": [
    {
      "model": "gpt-4o-mini",
      "prompt": "What is machine learning?",
      "response": "Machine learning is...",
      "latency_ms": 892.3,
      "tokens_used": 145,
      "cost_estimate": 0.0000218
    },
    {
      "model": "gpt-3.5-turbo",
      "prompt": "What is machine learning?",
      "response": "Machine learning is a...",
      "latency_ms": 643.1,
      "tokens_used": 138,
      "cost_estimate": 0.000276
    }
  ],
  "created_at": "2024-01-01T12:00:00Z"
}
```

---

## Health Check

### GET /health
Check API health (no auth required).

**Response (200):**
```json
{
  "status": "healthy",
  "service": "arvesha-research-api",
  "version": "1.0.0"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message here"
}
```

| Status Code | Meaning |
|-------------|---------|
| 400 | Bad Request (validation error, duplicate) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (not allowed) |
| 404 | Not Found |
| 422 | Unprocessable Entity (Pydantic validation) |
| 500 | Internal Server Error |
