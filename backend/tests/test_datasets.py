import pytest
from httpx import AsyncClient


async def _get_token(client: AsyncClient, username: str = "dsuser") -> str:
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
async def test_list_datasets_empty(client: AsyncClient):
    token = await _get_token(client)
    resp = await client.get("/api/v1/datasets/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_upload_txt_file(client: AsyncClient):
    token = await _get_token(client, "uploader")
    files = {"file": ("test.txt", b"Hello world this is a test document.", "text/plain")}
    resp = await client.post(
        "/api/v1/datasets/upload",
        files=files,
        data={"description": "test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "test.txt"
    assert data["file_type"] == "txt"
