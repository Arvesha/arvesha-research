from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.api import auth, research, datasets, rag, agents, benchmarks
from app.core.config import settings
from app.core.database import create_all_tables
from app.core.middleware import RequestIDMiddleware, LoggingMiddleware
from app.core.logging import configure_logging

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await create_all_tables()
    logger.info("arvesha-research backend started", version="1.0.0")
    yield
    logger.info("arvesha-research backend shutting down")


app = FastAPI(
    title="Arvesha Research API",
    description="AI Research Platform by Arvesha Intelligence",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(research.router, prefix="/api/v1/research", tags=["research"])
app.include_router(datasets.router, prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(benchmarks.router, prefix="/api/v1/benchmark", tags=["benchmarks"])


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "service": "arvesha-research-api", "version": "1.0.0"}
