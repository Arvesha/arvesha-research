import io
import os
import uuid
from typing import List
import structlog
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import Dataset, Document, User
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.base import BaseRepository
from app.utils.helpers import chunk_text as _chunk_text

logger = structlog.get_logger()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _parse_file(content: bytes, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "txt":
        return content.decode("utf-8", errors="ignore")
    elif ext == "csv":
        import pandas as pd
        df = pd.read_csv(io.BytesIO(content))
        return df.to_string()
    elif ext == "json":
        return content.decode("utf-8", errors="ignore")
    elif ext == "pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")


async def upload_dataset(file: UploadFile, description: str, user: User, db: AsyncSession) -> Dataset:
    content = await file.read()
    filename = file.filename or "upload.txt"
    ext = filename.rsplit(".", 1)[-1].lower()

    text = _parse_file(content, filename)
    chunks = _chunk_text(text)

    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{filename}")
    with open(file_path, "wb") as f:
        f.write(content)

    dataset = Dataset(
        name=filename,
        description=description,
        file_type=ext,
        file_path=file_path,
        chunks_count=len(chunks),
        user_id=user.id,
    )
    repo = DatasetRepository(db)
    dataset = await repo.create(dataset)

    # Store documents
    doc_repo = BaseRepository(Document, db)
    try:
        from app.services import embedding_service, vector_store_service
        embeddings = embedding_service.embed_batch(chunks)
        ids = [str(uuid.uuid4()) for _ in chunks]
        vector_store_service.add_documents(
            collection_name="arvesha_research",
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"dataset_id": dataset.id, "chunk_index": i} for i in range(len(chunks))],
            ids=ids,
        )
        for i, (chunk, emb_id) in enumerate(zip(chunks, ids)):
            doc = Document(
                dataset_id=dataset.id,
                content=chunk,
                embedding_id=emb_id,
                chunk_index=i,
                doc_metadata={"chunk_index": i},
            )
            await doc_repo.create(doc)
    except Exception as e:
        logger.warning("vector store unavailable, storing text only", error=str(e))
        for i, chunk in enumerate(chunks):
            doc = Document(
                dataset_id=dataset.id,
                content=chunk,
                chunk_index=i,
                doc_metadata={"chunk_index": i},
            )
            await doc_repo.create(doc)

    logger.info("dataset uploaded", dataset_id=dataset.id, chunks=len(chunks))
    return dataset


async def list_datasets(user: User, db: AsyncSession) -> list[Dataset]:
    repo = DatasetRepository(db)
    return await repo.get_by_user(user.id)


async def delete_dataset(dataset_id: int, user: User, db: AsyncSession) -> None:
    repo = DatasetRepository(db)
    dataset = await repo.get_by_id(dataset_id)
    if not dataset or dataset.user_id != user.id:
        raise HTTPException(status_code=404, detail="Dataset not found")
    await repo.delete(dataset)
