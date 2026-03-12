import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock, AsyncMock


async def _get_token(client: AsyncClient, username: str = "raguser") -> str:
    await client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": f"{username}@example.com", "password": "pass123"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"username": username, "password": "pass123"},
    )
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_rag_query_no_stream(client: AsyncClient):
    token = await _get_token(client)
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test answer"))]
    mock_response.usage = MagicMock(total_tokens=50)

    with patch("app.services.embedding_service.embed_text", return_value=[0.1] * 384), \
         patch("app.services.vector_store_service.query_similar", return_value={
             "documents": [[]], "distances": [[]], "metadatas": [[]]
         }), \
         patch("openai.AsyncOpenAI") as mock_openai:
        mock_client = AsyncMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        resp = await client.post(
            "/api/v1/rag/query",
            json={"query": "What is RAG?", "stream": False},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data
    assert "sources" in data
