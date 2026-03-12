import time
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import ResearchExperiment, User
from app.repositories.experiment_repository import ExperimentRepository
from app.schemas.research import CreateExperimentRequest, PromptTestRequest, PromptTestResponse


async def create_experiment(request: CreateExperimentRequest, user: User, db: AsyncSession) -> ResearchExperiment:
    repo = ExperimentRepository(db)
    experiment = ResearchExperiment(
        title=request.title,
        description=request.description,
        dataset=request.dataset,
        model=request.model,
        prompt_template=request.prompt_template,
        user_id=user.id,
    )
    return await repo.create(experiment)


async def list_experiments(user: User, db: AsyncSession) -> list[ResearchExperiment]:
    repo = ExperimentRepository(db)
    return await repo.get_by_user(user.id)


async def get_experiment(experiment_id: int, user: User, db: AsyncSession) -> ResearchExperiment:
    repo = ExperimentRepository(db)
    experiment = await repo.get_by_id(experiment_id)
    if not experiment or experiment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    return experiment


async def delete_experiment(experiment_id: int, user: User, db: AsyncSession) -> None:
    repo = ExperimentRepository(db)
    experiment = await repo.get_by_id(experiment_id)
    if not experiment or experiment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")
    await repo.delete(experiment)


async def test_prompt(request: PromptTestRequest) -> PromptTestResponse:
    from openai import AsyncOpenAI
    from app.core.config import settings

    start = time.perf_counter()
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY or "dummy", base_url=settings.OPENAI_BASE_URL)
    try:
        resp = await client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            temperature=request.temperature,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000
        return PromptTestResponse(
            response=resp.choices[0].message.content or "",
            tokens_used=resp.usage.total_tokens if resp.usage else 0,
            latency_ms=round(elapsed_ms, 2),
        )
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return PromptTestResponse(response=f"Error: {str(e)}", tokens_used=0, latency_ms=round(elapsed_ms, 2))
