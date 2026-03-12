from typing import List, Optional
from pydantic import BaseModel


class AgentStep(BaseModel):
    step: int
    action: str
    observation: str


class AgentRunRequest(BaseModel):
    agent_type: str = "research"  # research | summarization | data_extraction
    input: str
    tools: List[str] = []


class AgentRunResponse(BaseModel):
    output: str
    steps: List[AgentStep]
    tokens_used: int
    agent_type: str
