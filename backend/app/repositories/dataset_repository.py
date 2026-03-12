from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.db import Dataset
from app.repositories.base import BaseRepository


class DatasetRepository(BaseRepository[Dataset]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Dataset, db)

    async def get_by_user(self, user_id: int) -> List[Dataset]:
        result = await self.db.execute(
            select(Dataset)
            .where(Dataset.user_id == user_id)
            .order_by(Dataset.created_at.desc())
        )
        return list(result.scalars().all())
