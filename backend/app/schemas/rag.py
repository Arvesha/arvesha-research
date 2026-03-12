from typing import Optional, List
from pydantic import BaseModel


class Source(BaseModel):
    content: str
    document_id: Optional[str] = None
    score: float = 0.0
    metadata: dict = {}


class RAGQueryRequest(BaseModel):
    query: str
    dataset_id: Optional[int] = None
    top_k: int = 5
    use_rerank: bool = True
    stream: bool = False


class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    tokens_used: int
    latency_ms: float
