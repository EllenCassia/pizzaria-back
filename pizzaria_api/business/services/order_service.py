from typing import List
from pizzaria_api.model.entity.models import Order
from pizzaria_api.model.repository.order_repository import OrderRepository
from pizzaria_api.model.repository.product_repository import ProductRepository
from pizzaria_api.model.schemas.pedido_schemas import PedidoResponse, PedidoSchema
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError


class OrderService:

    def __init__(self, session):
        self.order_repository = OrderRepository(session)
        self.product_repository = ProductRepository(session)

    async def create_order(self, pedido_data: PedidoSchema) -> PedidoResponse:
        # Obtenha apenas os produtos que foram passados pelo pedido
        products = await self.product_repository.get_products_by_ids(pedido_data.product_ids)

        if not products:
            raise ObjectSaveError("No valid products found for the order")

        new_order = Order(
            number_table=pedido_data.number_table,
            amount=pedido_data.amount,  
            products=products  
        )

        try:
            created_order = await self.order_repository.create_order(new_order)
        
            return PedidoResponse(
                id=created_order.id,
                number_table=created_order.number_table,
                amount=created_order.amount,
                product_ids=[product.pk_id for product in created_order.products] 
            )
        except Exception as e:
            raise ObjectSaveError(f"Unable to save the object due to an unexpected error: {e}")
        
    async def get_all_orders(self) -> List[PedidoResponse]:
        try:
            orders = await self.order_repository.get_all_orders()
            return [
                PedidoResponse(
                    id=order.id,
                    number_table=order.number_table,
                    amount=order.amount,
                    product_ids=[product.pk_id for product in order.products]
                ) for order in orders
            ]
        except Exception as e:
            raise ObjectSaveError(f"Unable to get the orders due to an unexpected error: {e}")
