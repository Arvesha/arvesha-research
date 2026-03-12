import pytest
from httpx import AsyncClient


async def _get_token(client: AsyncClient, username: str = "researcher") -> str:
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
async def test_create_experiment(client: AsyncClient):
    token = await _get_token(client)
    resp = await client.post(
        "/api/v1/research/experiment",
        json={"title": "Test Experiment", "model": "gpt-4o-mini", "description": "A test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Experiment"


@pytest.mark.asyncio
async def test_list_experiments(client: AsyncClient):
    token = await _get_token(client, "lister")
    await client.post(
        "/api/v1/research/experiment",
        json={"title": "Exp 1", "model": "gpt-4o-mini"},
        headers={"Authorization": f"Bearer {token}"},
    )
    resp = await client.get("/api/v1/research/experiments", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@pytest.mark.asyncio
async def test_delete_experiment(client: AsyncClient):
    token = await _get_token(client, "deleter")
    create_resp = await client.post(
        "/api/v1/research/experiment",
        json={"title": "To Delete", "model": "gpt-4o-mini"},
        headers={"Authorization": f"Bearer {token}"},
    )
    exp_id = create_resp.json()["id"]
    del_resp = await client.delete(
        f"/api/v1/research/experiment/{exp_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert del_resp.status_code == 204


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    resp = await client.get("/api/v1/research/experiments")
    assert resp.status_code in (401, 403)
