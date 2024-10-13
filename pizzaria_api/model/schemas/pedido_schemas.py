from typing import List, Annotated
from pydantic import BaseModel, Field
from uuid import UUID

class PedidoSchema(BaseModel):
    number_table: Annotated[int, Field(ge=1, description="Número da mesa", examples=[56])]
    amount: Annotated[float, Field(ge=1, description="Quantidade do produto", examples=[1.0])]  # Alterado para float se for valor monetário
    product_ids: Annotated[List[int], Field(description="Lista de IDs dos produtos", examples=[[1, 2, 3]])]

class PedidoResponse(BaseModel):
    id: UUID  # Ou str, dependendo de como você está gerenciando os IDs
    number_table: Annotated[int, Field(ge=1, description="Número da mesa", examples=[56])]
    amount: Annotated[float, Field(ge=1, description="Quantidade do produto", examples=[1.0])]  # Alterado para float
    product_ids: Annotated[List[int], Field(description="Lista de IDs dos produtos", examples=[[1, 2, 3]])]
