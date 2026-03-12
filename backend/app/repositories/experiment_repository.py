from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.db import ResearchExperiment
from app.repositories.base import BaseRepository


class ExperimentRepository(BaseRepository[ResearchExperiment]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(ResearchExperiment, db)

    async def get_by_user(self, user_id: int, limit: int = 100, offset: int = 0) -> List[ResearchExperiment]:
        result = await self.db.execute(
            select(ResearchExperiment)
            .where(ResearchExperiment.user_id == user_id)
            .order_by(ResearchExperiment.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
