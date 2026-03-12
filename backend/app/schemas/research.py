from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreateExperimentRequest(BaseModel):
    title: str
    description: Optional[str] = None
    dataset: Optional[str] = None
    model: str
    prompt_template: Optional[str] = None


class ExperimentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    dataset: Optional[str]
    model: str
    prompt_template: Optional[str]
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}


class PromptTestRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7


class PromptTestResponse(BaseModel):
    response: str
    tokens_used: int
    latency_ms: float
