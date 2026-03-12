from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DatasetResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    file_type: str
    chunks_count: int
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}


class UploadDatasetResponse(BaseModel):
    id: int
    name: str
    file_type: str
    chunks_count: int
    message: str
