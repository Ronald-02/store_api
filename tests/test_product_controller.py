import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products", json={
            "name": "Notebook Gamer",
            "description": "RTX 4070",
            "price": 7899.90
        })
    assert response.status_code == 201
    assert "id" in response.json()
