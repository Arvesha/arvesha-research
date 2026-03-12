from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.db import User
from app.schemas.research import CreateExperimentRequest, ExperimentResponse, PromptTestRequest, PromptTestResponse
from app.services.research_service import create_experiment, list_experiments, get_experiment, delete_experiment, test_prompt

router = APIRouter()


@router.post("/experiment", response_model=ExperimentResponse, status_code=201)
async def create(
    request: CreateExperimentRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_experiment(request, user, db)


@router.get("/experiments", response_model=List[ExperimentResponse])
async def list_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await list_experiments(user, db)


@router.get("/experiment/{id}", response_model=ExperimentResponse)
async def get_one(id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await get_experiment(id, user, db)


@router.delete("/experiment/{id}", status_code=204)
async def delete(id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_experiment(id, user, db)


@router.post("/test-prompt", response_model=PromptTestResponse)
async def run_prompt_test(request: PromptTestRequest, user: User = Depends(get_current_user)):
    return await test_prompt(request)
