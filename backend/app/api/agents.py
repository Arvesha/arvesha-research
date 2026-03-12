from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.db import User
from app.schemas.agents import AgentRunRequest, AgentRunResponse
from app.services.agent_service import run_agent

router = APIRouter()


@router.post("/run", response_model=AgentRunResponse)
async def run(request: AgentRunRequest, user: User = Depends(get_current_user)):
    return await run_agent(request)
