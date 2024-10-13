from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pizzaria_api.model.entity.models import Product


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: Product) -> Product:
        try:
            async with self.session.begin():
                self.session.add(product)  # Adiciona o produto
                await self.session.flush()  # Garante que o ID seja gerado antes de confirmar
                await self.session.commit()
                return product
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error adding product: {e}")
        finally:
            await self.session.close()

    async def get_product(self, product_id: int) -> Product:
        try:
            stmt = select(Product).filter(Product.pk_id == product_id)
            result = await self.session.execute(stmt)
            product = result.scalars().first()  # Obtém o primeiro resultado
            return product
        except Exception as e:
            raise Exception(f"Error getting product: {e}")
        finally:
            await self.session.close()

    async def get_all_products(self) -> list[Product]:
        try:
            stmt = select(Product)
            result = await self.session.execute(stmt)
            products = result.scalars().all()  # Obtém todos os resultados
            return products
        except Exception as e:
            raise Exception(f"Error getting products: {e}")
        finally:
            await self.session.close()  

    async def get_products_by_ids(self, product_ids: list[int]) -> list[Product]:
        try:
            stmt = select(Product).filter(Product.pk_id.in_(product_ids))
            result = await self.session.execute(stmt)
            products = result.scalars().all()  # Obtém todos os resultados
            return products
        except Exception as e:
            raise Exception(f"Error getting products: {e}")
        finally:
            await self.session.close()
