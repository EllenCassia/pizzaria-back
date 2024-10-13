from pizzaria_api.model.repository.categories_repository import CategoryRepository
from pizzaria_api.model.schemas.categoria_schemas import CategorySchema
from pizzaria_api.model.entity.models import Category  # Importe a classe SQLAlchemy Category
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError

class CategoryServices:

    def __init__(self, session):
        self.category_repository = CategoryRepository(session)

    async def create_category(self, category_data: CategorySchema) -> CategorySchema:
        try:
            # Converta CategorySchema para Category
            new_category = Category(
                name=category_data.name
            )
            created_category = await self.category_repository.create_category(new_category)
            return CategorySchema(
                name=created_category.name
            )
        except Exception as e:
            raise ObjectSaveError(f"Unable to save the object due to an unexpected error. {e}")

    async def get_all_categories(self) -> list[CategorySchema]:
        try:
            categories = await self.category_repository.get_all_categories()
            return [CategorySchema(
                name=category.name
            ) for category in categories]
        except Exception as e:
            raise Exception(f"Error getting categories: {e}")
