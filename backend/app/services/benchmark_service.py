import asyncio
import time
from typing import List
import structlog

from app.models.db import Benchmark, User
from app.schemas.benchmarks import BenchmarkRunRequest, BenchmarkRunResponse, BenchmarkResult
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger()

# Simple cost estimates per 1k tokens (USD)
COST_PER_1K = {
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
    "gpt-3.5-turbo": 0.002,
}


async def _run_single(model: str, prompt: str) -> BenchmarkResult:
    from openai import AsyncOpenAI
    from app.core.config import settings

    start = time.perf_counter()
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY or "dummy", base_url=settings.OPENAI_BASE_URL)
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        tokens = resp.usage.total_tokens if resp.usage else 0
        response_text = resp.choices[0].message.content or ""
        cost = (tokens / 1000) * COST_PER_1K.get(model, 0.002)
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        tokens = 0
        response_text = f"Error: {str(e)}"
        cost = 0.0

    return BenchmarkResult(
        model=model,
        prompt=prompt[:100],
        response=response_text,
        latency_ms=round(elapsed_ms, 2),
        tokens_used=tokens,
        cost_estimate=round(cost, 6),
    )


async def run_benchmark(request: BenchmarkRunRequest, user: User, db: AsyncSession) -> BenchmarkRunResponse:
    from app.repositories.base import BaseRepository

    tasks = [_run_single(model, prompt) for model in request.models for prompt in request.prompts]
    results: List[BenchmarkResult] = await asyncio.gather(*tasks)

    repo = BaseRepository(Benchmark, db)
    benchmark = Benchmark(
        name=request.name,
        models=request.models,
        prompts=request.prompts,
        results=[r.model_dump() for r in results],
        user_id=user.id,
    )
    benchmark = await repo.create(benchmark)

    return BenchmarkRunResponse(
        id=benchmark.id,
        name=benchmark.name,
        results=results,
        created_at=benchmark.created_at,
    )
