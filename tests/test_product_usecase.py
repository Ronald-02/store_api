import pytest
from datetime import datetime
from app.usecases.product_usecase import ProductUsecase
from app.schemas.product_schema import ProductCreate


@pytest.mark.asyncio
async def test_create_product_success(mocker):
    # Simula o insert no banco com retorno de _id falso
    mock_db = mocker.AsyncMock()
    mock_db.products.insert_one.return_value.inserted_id = "fakeid123"

    usecase = ProductUsecase(mock_db)

    product_data = ProductCreate(
        name="Notebook Gamer",
        description="RTX 4060, i7",
        price=7500.0
    )

    result = await usecase.create_product(product_data)

    assert result["name"] == "Notebook Gamer"
    assert "created_at" in result
    assert result["_id"] == "fakeid123"


@pytest.mark.asyncio
async def test_get_product_not_found(mocker):
    # Simula busca sem encontrar produto
    mock_db = mocker.AsyncMock()
    mock_db.products.find_one.return_value = None

    usecase = ProductUsecase(mock_db)

    result = await usecase.get_product("invalid_id")

    assert result is None


@pytest.mark.asyncio
async def test_update_product_success(mocker):
    # Simula atualização com sucesso
    mock_db = mocker.AsyncMock()
    mock_db.products.find_one_and_update.return_value = {
        "_id": "fakeid123",
        "name": "Notebook Gamer",
        "description": "RTX 4060, i7",
        "price": 8000.0,
        "updated_at": datetime.utcnow()
    }

    usecase = ProductUsecase(mock_db)

    result = await usecase.update_product("fakeid123", {"price": 8000.0})

    assert result["price"] == 8000.0
    assert "updated_at" in result


@pytest.mark.asyncio
async def test_delete_product_success(mocker):
    # Simula deleção bem-sucedida
    mock_db = mocker.AsyncMock()
    mock_db.products.delete_one.return_value.deleted_count = 1

    usecase = ProductUsecase(mock_db)

    result = await usecase.delete_product("fakeid123")

    assert result is True


@pytest.mark.asyncio
async def test_delete_product_not_found(mocker):
    # Simula deleção sem encontrar o documento
    mock_db = mocker.AsyncMock()
    mock_db.products.delete_one.return_value.deleted_count = 0

    usecase = ProductUsecase(mock_db)

    result = await usecase.delete_product("fakeid123")

    assert result is False
