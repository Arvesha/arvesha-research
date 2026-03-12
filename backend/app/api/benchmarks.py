from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.db import User
from app.schemas.benchmarks import BenchmarkRunRequest, BenchmarkRunResponse
from app.services.benchmark_service import run_benchmark

router = APIRouter()


@router.post("/run", response_model=BenchmarkRunResponse, status_code=201)
async def run(
    request: BenchmarkRunRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await run_benchmark(request, user, db)
