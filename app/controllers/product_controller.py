from fastapi import APIRouter, HTTPException, Query
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.usecases import product_usecase

router = APIRouter()


# Criar produto
@router.post("/products", status_code=201)
async def create_product(data: ProductCreate):
    try:
        product_id = await product_usecase.create_product(data)
        return {"id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Listar produtos com filtros opcionais de preço
@router.get("/products")
async def list_products(
    min_price: float = Query(default=None, gt=0),
    max_price: float = Query(default=None, gt=0),
):
    try:
        return await product_usecase.list_products(min_price=min_price, max_price=max_price)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obter detalhes de um produto específico
@router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await product_usecase.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Converter MongoDB ObjectId para string (se necessário)
    product["id"] = str(product["_id"])
    del product["_id"]

    return product


# Atualizar completamente um produto
@router.put("/products/{product_id}")
async def update_product(product_id: str, data: ProductUpdate):
    try:
        await product_usecase.update_product(product_id, data)
        return {"message": "Produto atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Atualização parcial de um produto
@router.patch("/products/{product_id}")
async def patch_product(product_id: str, data: ProductUpdate):
    try:
        await product_usecase.patch_product(product_id, data)
        return {"message": "Produto atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Deletar um produto
@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: str):
    try:
        await product_usecase.delete_product(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
