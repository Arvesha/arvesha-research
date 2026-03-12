from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class BenchmarkRunRequest(BaseModel):
    name: str = "benchmark"
    models: List[str]
    prompts: List[str]
    metrics: List[str] = ["latency", "tokens", "cost"]


class BenchmarkResult(BaseModel):
    model: str
    prompt: str
    response: str
    latency_ms: float
    tokens_used: int
    cost_estimate: float


class BenchmarkRunResponse(BaseModel):
    id: int
    name: str
    results: List[BenchmarkResult]
    created_at: datetime
