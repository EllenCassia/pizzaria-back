from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from pizzaria_api.model.entity.models import Category

class CategoryRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, category: Category) -> Category:
        try:
            async with self.session.begin():
                self.session.add(category) # Adiciona a categoria
                await self.session.flush()  # Garante que o ID seja gerado antes de confirmar
                await self.session.commit()
                return category
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error adding category: {e}")
        finally:
            await self.session.close()    

    # async def get_category(self, category_id: int) -> Category:
    #     try:
    #         stmt = select(Category).filter(Category.pk_id == category_id)
    #         result = await self.session.execute(stmt)
    #         category = result.scalars().first()  # Use scalars().first() para obter o primeiro resultado
    #         return category
    #     except Exception as e:
    #         raise Exception(f"Error getting category: {e}")
    #     finally:
    #         await self.session.close()

    # async def delete_category(self, category_id: str) -> Category:
    #     try:
    #         category = await self.get_category(category_id)
    #         if not category:
    #             raise Exception("Category not found.")
    #         await self.session.delete(category) # Deleta a categoria
    #         await self.session.commit()
    #         return category
    #     except Exception as e:
    #         await self.session.rollback()
    #         raise Exception(f"Error deleting category: {e}")
    #     finally:
    #         await self.session.close()

    async def get_all_categories(self) -> list[Category]:
        try:
            stmt = select(Category)
            result = await self.session.execute(stmt) # Executa a consulta no banco de dados e retorna um objeto Result 
            categories = result.scalars().all() # Use scalars().all() para obter todos os resultados
            return categories
        except Exception as e:
            raise Exception(f"Error getting categories: {e}")
        finally:
            await self.session.close()

    # async def update_category(self, category: Category) -> Category:
    #     try:
    #         async with self.session.begin():
    #             self.session.merge(category) # Atualiza a categoria
    #             await self.session.flush()  # Garante que o ID seja gerado antes de confirmar
    #             await self.session.commit()
    #             return category
    #     except Exception as e:
    #         await self.session.rollback()
    #         raise Exception(f"Error updating category: {e}")
    #     finally:
    #         await self.session.close()
                            