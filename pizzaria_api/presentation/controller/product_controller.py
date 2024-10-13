from fastapi import APIRouter, Depends
from pizzaria_api.business.services.product_services import ProductService
from pizzaria_api.infra.database.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from pizzaria_api.model.schemas.produto_schemas import ProductResponse, ProductSchema
from pizzaria_api.presentation.controller.user_controller import validate_token
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=201, summary="Cria um produto")
async def create_product(
    product: ProductSchema,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token)
) -> ProductResponse:
    try:
        product_service = ProductService(session)
        created_product = await product_service.create_product(product)
        return created_product
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.get("/", response_model=list[ProductResponse], summary="Lista todos os produtos")
async def list_products(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token)
) -> list[ProductResponse]:
    try:
        product_service = ProductService(session)
        products = await product_service.get_all_products()
        return products
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.get("/{product_id}", response_model=ProductResponse, summary="Obtém um produto")
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token)
) -> ProductResponse:
    try:
        product_service = ProductService(session)
        product = await product_service.get_product(product_id)
        return product
    except ObjectSaveError as e:
        print(f"Error: {e}")      

