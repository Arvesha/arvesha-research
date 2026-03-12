import time
from typing import AsyncGenerator, List
import structlog

from app.schemas.rag import RAGQueryRequest, RAGQueryResponse, Source

logger = structlog.get_logger()


async def query_rag(request: RAGQueryRequest) -> RAGQueryResponse:
    from app.core.config import settings
    from app.services.embedding_service import embed_text
    from app.services.vector_store_service import query_similar
    from openai import AsyncOpenAI

    start = time.perf_counter()

    # Embed query
    try:
        query_embedding = embed_text(request.query)
    except Exception as e:
        logger.warning("embedding failed", error=str(e))
        query_embedding = [0.0] * 384

    # Vector search
    where_filter = {"dataset_id": request.dataset_id} if request.dataset_id else None
    try:
        results = query_similar(
            collection_name="arvesha_research",
            query_embedding=query_embedding,
            top_k=request.top_k,
            where_filter=where_filter,
        )
        docs = results["documents"][0] if results.get("documents") else []
        dists = results["distances"][0] if results.get("distances") else []
        metas = results["metadatas"][0] if results.get("metadatas") else []
    except Exception as e:
        logger.warning("vector search failed", error=str(e))
        docs, dists, metas = [], [], []

    # Rerank: sort by distance (lower distance = better match), then convert to similarity score
    if request.use_rerank and docs:
        scored = list(zip(docs, dists, metas))
        scored.sort(key=lambda x: x[1])  # ascending distance = descending similarity
        docs, dists, metas = zip(*scored) if scored else ([], [], [])

    # score = 1.0 - distance (ChromaDB cosine distances are in [0, 2], so score ∈ [-1, 1])
    sources = [
        Source(content=doc, score=round(1.0 - float(dist), 4) if dist is not None else 0.0, metadata=meta or {})
        for doc, dist, meta in zip(docs, dists, metas)
    ]

    # Build context
    context = "\n\n".join(docs[:request.top_k]) if docs else "No relevant context found."
    system_prompt = "You are an AI research assistant. Answer based on the provided context."
    user_prompt = f"Context:\n{context}\n\nQuestion: {request.query}"

    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY or "dummy", base_url=settings.OPENAI_BASE_URL)
    try:
        resp = await client.chat.completions.create(
            model=settings.DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        answer = resp.choices[0].message.content or ""
        tokens_used = resp.usage.total_tokens if resp.usage else 0
    except Exception as e:
        answer = f"LLM unavailable: {str(e)}"
        tokens_used = 0

    elapsed_ms = (time.perf_counter() - start) * 1000
    return RAGQueryResponse(
        answer=answer,
        sources=sources,
        tokens_used=tokens_used,
        latency_ms=round(elapsed_ms, 2),
    )


async def stream_rag(request: RAGQueryRequest) -> AsyncGenerator[str, None]:
    from app.core.config import settings
    from app.services.embedding_service import embed_text
    from app.services.vector_store_service import query_similar
    from openai import AsyncOpenAI

    try:
        query_embedding = embed_text(request.query)
    except Exception:
        query_embedding = [0.0] * 384

    where_filter = {"dataset_id": request.dataset_id} if request.dataset_id else None
    try:
        results = query_similar("arvesha_research", query_embedding, request.top_k, where_filter)
        docs = results["documents"][0] if results.get("documents") else []
    except Exception:
        docs = []

    context = "\n\n".join(docs) if docs else "No relevant context found."
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY or "dummy", base_url=settings.OPENAI_BASE_URL)
    try:
        async with client.chat.completions.stream(
            model=settings.DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI research assistant."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.query}"},
            ],
        ) as stream:
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
    except Exception as e:
        yield f"data: Error: {str(e)}\n\n"
    yield "data: [DONE]\n\n"
