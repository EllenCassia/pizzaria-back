from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pizzaria_api.model.schemas.categoria_schemas import CategorySchema
from pizzaria_api.infra.database.connection import get_session
from pizzaria_api.business.services.category_services import CategoryServices
from pizzaria_api.presentation.controller.user_controller import validate_token


router = APIRouter()

@router.post("/", summary="Criação de uma nova categoria", response_model=CategorySchema)
async def create_category(
    category: CategorySchema, 
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token)  # Autenticação obrigatória
) -> CategorySchema:
    try:
        category_service = CategoryServices(session)
        category = await category_service.create_category(category)
        return category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", summary="Listagem de todas as categorias", response_model=list[CategorySchema])
async def list_categories(
    session: AsyncSession = Depends(get_session),
    token: str = Depends(validate_token)  
) -> list[CategorySchema]:
    try:
        category_service = CategoryServices(session)
        categories = await category_service.get_all_categories()
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
