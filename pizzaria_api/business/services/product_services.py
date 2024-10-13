from pizzaria_api.model.entity.models import Product
from pizzaria_api.model.repository.product_repository import ProductRepository
from pizzaria_api.model.schemas.produto_schemas import ProductResponse, ProductSchema
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError


class ProductService:

    def __init__(self, session):
        self.product_repository = ProductRepository(session)

    async def create_product(self, product_data: ProductSchema) -> ProductResponse:
        try:
            new_product = Product(
                name=product_data.name,
                price=product_data.price,
                describe=product_data.describe, 
                category_id=product_data.category_id
            )
            created_product = await self.product_repository.create_product(new_product)
            return ProductResponse(
                name=created_product.name,
                price=created_product.price,
                describe=created_product.describe 
            )
        except Exception as e:
            raise ObjectSaveError(f"Unable to save the object due to an unexpected error. {e}")

    async def get_product(self, product_id: int) -> ProductResponse:
        try:
            product = await self.product_repository.get_product(product_id)
            return ProductResponse(
                name=product.name,
                price=product.price,
                describe=product.describe
            )
        except Exception as e:
            raise Exception(f"Error getting product: {e}")
        
    async def get_all_products(self) -> list[ProductResponse]:
        try:
            products = await self.product_repository.get_all_products()
            return [ProductResponse(
                name=product.name,
                price=product.price,
                describe=product.describe
            ) for product in products]
        except Exception as e:
            raise Exception(f"Error getting products: {e}")    
          
