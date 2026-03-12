from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.db import User
from app.schemas.datasets import DatasetResponse, UploadDatasetResponse
from app.services.dataset_service import upload_dataset, list_datasets, delete_dataset

router = APIRouter()


@router.post("/upload", response_model=UploadDatasetResponse, status_code=201)
async def upload(
    file: UploadFile = File(...),
    description: str = Form(default=""),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    dataset = await upload_dataset(file, description, user, db)
    return UploadDatasetResponse(
        id=dataset.id,
        name=dataset.name,
        file_type=dataset.file_type,
        chunks_count=dataset.chunks_count,
        message="Dataset uploaded successfully",
    )


@router.get("/", response_model=List[DatasetResponse])
async def list_all(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await list_datasets(user, db)


@router.delete("/{id}", status_code=204)
async def delete(id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await delete_dataset(id, user, db)
