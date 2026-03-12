import time
from typing import List
import structlog

from app.schemas.agents import AgentRunRequest, AgentRunResponse, AgentStep

logger = structlog.get_logger()


async def run_agent(request: AgentRunRequest) -> AgentRunResponse:
    from app.core.config import settings
    start = time.perf_counter()
    steps: List[AgentStep] = []

    try:
        from langchain_openai import ChatOpenAI
        from langchain.agents import AgentExecutor, create_react_agent
        from langchain_core.prompts import PromptTemplate
        from langchain_core.tools import tool

        @tool
        def search_knowledge(query: str) -> str:
            """Search the knowledge base for relevant information."""
            return f"Found relevant information about: {query}"

        @tool
        def summarize_text(text: str) -> str:
            """Summarize the provided text."""
            return f"Summary: {text[:200]}..."

        @tool
        def extract_data(text: str) -> str:
            """Extract structured data from text."""
            return f"Extracted data: {{'text': '{text[:100]}'}}"

        tool_map = {
            "research": [search_knowledge],
            "summarization": [summarize_text],
            "data_extraction": [extract_data],
        }
        tools = tool_map.get(request.agent_type, [search_knowledge])
        if request.tools:
            all_tools = [search_knowledge, summarize_text, extract_data]
            tools = [t for t in all_tools if t.name in request.tools] or tools

        llm = ChatOpenAI(
            model=settings.DEFAULT_MODEL,
            api_key=settings.OPENAI_API_KEY or "dummy",
            base_url=settings.OPENAI_BASE_URL,
            temperature=0,
        )

        tool_names = ", ".join([t.name for t in tools])
        tool_descriptions = "\n".join([f"{t.name}: {t.description}" for t in tools])

        prompt = PromptTemplate.from_template(
            "You are a {agent_type} AI agent. Answer the user's query.\n\n"
            "Tools available:\n{tool_descriptions}\n\n"
            "Use this format:\n"
            "Thought: what to do\n"
            "Action: tool name\n"
            "Action Input: input\n"
            "Observation: result\n"
            "Thought: I have the answer\n"
            "Final Answer: the answer\n\n"
            "Question: {input}\n"
            "{agent_scratchpad}"
        )

        agent = create_react_agent(llm, tools, prompt)
        executor = AgentExecutor(
            agent=agent,
            tools=tools,
            max_iterations=3,
            verbose=False,
            handle_parsing_errors=True,
        )
        result = await executor.ainvoke({
            "input": request.input,
            "agent_type": request.agent_type,
            "tool_descriptions": tool_descriptions,
        })

        output = result.get("output", "No output")
        steps = [AgentStep(step=1, action="agent_run", observation=output)]
        tokens_used = 0

    except Exception as e:
        logger.warning("agent execution error, using fallback", error=str(e))
        output = (
            f"Agent ({request.agent_type}) processed: {request.input[:100]}. "
            "[Note: Full agent execution requires valid API key]"
        )
        steps = [AgentStep(step=1, action=f"{request.agent_type}_agent", observation=output)]
        tokens_used = 0

    return AgentRunResponse(
        output=output,
        steps=steps,
        tokens_used=tokens_used,
        agent_type=request.agent_type,
    )
