from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from requests import session
from pizzaria_api.business.services.user_services import UserService
from pizzaria_api.model.schemas.user_schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pizzaria_api.infra.database.connection import get_session
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
router = APIRouter()

@router.post("/",summary="Criação de um novo usuário", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    try:
        user_service = UserService(session)
        user = await user_service.create_user(user)
        return user
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.get("/{user_id}",summary="Busca de um usuário", response_model=UserResponse)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    try:
        user_service = UserService(session)
        user = await user_service.get_user(user_id)
        return user
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.get("/",summary="Busca de todos os usuários", response_model=list[UserResponse])
async def get_all_users(
    session: AsyncSession = Depends(get_session)
) -> list[UserResponse]:
    try:
        user_service = UserService(session)
        users = await user_service.get_all_users()
        return users
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.put("/{user_id}",summary="Atualização de um usuário", response_model=UserResponse)
async def update_user(
    user_id: int, 
    user: UserCreate, 
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    try:
        user_service = UserService(session)
        user = await user_service.update_user(user_id, user)
        return user
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.delete("/{user_id}",summary="Deletar um usuário", response_model=UserResponse)
async def delete_user(
    user_id: int, 
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    try:
        user_service = UserService(session)
        user = await user_service.delete_user(user_id)
        return user
    except ObjectSaveError as e:
        print(f"Error: {e}")

@router.post("/login", summary="Login de um usuário", response_model=TokenResponse)
async def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    try:
        user_service = UserService(session)
        user = UserLogin(
            email=login_request_form.username,
            password=login_request_form.password
        )
        token_data = await user_service.user_login(user=user, expire_in=60)
        return token_data
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/validate-token", summary="Valida o token do usuário")
async def validate_token(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session
)):
    try:
        user_service = UserService(session)
        user_email = await user_service.verify_token(token)
        return {"email": user_email}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")    