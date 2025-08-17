from datetime import datetime
from bson import ObjectId
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductUsecase:
    def __init__(self, db):
        self.db = db
        self.collection = db.products

    # Criar um novo produto
    async def create_product(self, product: ProductCreate):
        data = product.dict()
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = None

        result = await self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data

    # Buscar produto por ID
    async def get_product(self, product_id: str):
        if not ObjectId.is_valid(product_id):
            return None

        product = await self.collection.find_one({"_id": ObjectId(product_id)})
        if product:
            product["_id"] = str(product["_id"])
        return product

    # Listar todos os produtos
    async def list_products(self):
        cursor = self.collection.find({})
        products = []
        async for product in cursor:
            product["_id"] = str(product["_id"])
            products.append(product)
        return products

    # Atualizar um produto existente
    async def update_product(self, product_id: str, product_update: dict):
        if not ObjectId.is_valid(product_id):
            return None

        product_update["updated_at"] = datetime.utcnow()

        updated_product = await self.collection.find_one_and_update(
            {"_id": ObjectId(product_id)},
            {"$set": product_update},
            return_document=True  # Garantir retorno do documento atualizado
        )

        if updated_product:
            updated_product["_id"] = str(updated_product["_id"])
        return updated_product

    # Deletar um produto
    async def delete_product(self, product_id: str):
        if not ObjectId.is_valid(product_id):
            return False

        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
