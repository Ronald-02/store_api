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


@pytest.mark.asyncio
async def test_filter_products_by_price():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Criando produtos de teste
        await ac.post("/products", json={
            "name": "Produto A",
            "description": "Barato",
            "price": 1000
        })
        await ac.post("/products", json={
            "name": "Produto B",
            "description": "Ideal",
            "price": 6000
        })

        # Filtrando produtos por faixa de preço
        response = await ac.get("/products?min_price=5000&max_price=8000")
        data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(5000 < prod["price"] < 8000 for prod in data)


@pytest.mark.asyncio
async def test_patch_product_sets_updated_at():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Criando produto
        create_response = await ac.post("/products", json={
            "name": "Mouse Gamer",
            "description": "Alta precisão",
            "price": 199.99
        })
        product_id = create_response.json()["id"]

        # Atualizando parcialmente (patch)
        patch_response = await ac.patch(f"/products/{product_id}", json={
            "price": 249.99
        })

        # Recuperando produto atualizado
        get_response = await ac.get(f"/products/{product_id}")
        product = get_response.json()

    assert patch_response.status_code == 200
    assert "updated_at" in product
