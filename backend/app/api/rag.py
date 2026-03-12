from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.security import get_current_user
from app.models.db import User
from app.schemas.rag import RAGQueryRequest, RAGQueryResponse
from app.services.rag_service import query_rag, stream_rag

router = APIRouter()


@router.post("/query")
async def rag_query(request: RAGQueryRequest, user: User = Depends(get_current_user)):
    if request.stream:
        return StreamingResponse(stream_rag(request), media_type="text/event-stream")
    return await query_rag(request)
