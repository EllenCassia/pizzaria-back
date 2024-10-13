from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pizzaria_api.business.services.order_service import OrderService
from pizzaria_api.model.schemas.pedido_schemas import PedidoSchema, PedidoResponse
from pizzaria_api.infra.database.connection import get_session
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError

router = APIRouter()

@router.post("/", response_model=PedidoResponse, summary="Cria um pedido")
async def create_order(
    order: PedidoSchema,
    session: AsyncSession = Depends(get_session)
) -> PedidoResponse:
    try:
        order_service = OrderService(session)
        created_order = await order_service.create_order(order)
        return created_order
    except ObjectSaveError as e:
        print(f"Error: {e}")
        raise e
    
@router.get("/", response_model=list[PedidoResponse], summary="Obtém todos os pedidos")
async def get_all_orders(
    session: AsyncSession = Depends(get_session)
) -> list[PedidoResponse]:
    try:
        order_service = OrderService(session)
        orders = await order_service.get_all_orders()
        return orders
    except ObjectSaveError as e:
        print(f"Error: {e}")
        raise e
        