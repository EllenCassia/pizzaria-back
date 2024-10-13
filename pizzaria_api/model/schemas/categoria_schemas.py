from pydantic import BaseModel, Field
from typing import Annotated

class CategorySchema(BaseModel):
    name: Annotated[str, Field(description="Nome da Categoria", example="Porções")]