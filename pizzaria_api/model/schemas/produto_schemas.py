from pydantic import BaseModel, Field
from typing import Annotated

class ProductSchema(BaseModel):
    name: Annotated[str, Field(description="Nome do Produto", example="Pizza de Calabresa")]
    price: Annotated[float, Field(description="Preço do produto", example=52.00)]  
    describe: Annotated[str, Field(description="Descrição do produto", example="Pizza de Calabresa com cebola, azeitona e orégano")]
    category_id: Annotated[int, Field(description="ID da categoria", example=1)]

class ProductResponse(BaseModel):
    name: Annotated[str, Field(description="Nome do Produto", example="Pizza de Calabresa")]
    price: Annotated[float, Field(description="Preço do produto", example=52.00)]
    describe: Annotated[str, Field(description="Descrição do produto", example="Pizza de Calabresa com cebola, azeitona e orégano")]
