from datetime import datetime, timedelta 
from http.client import HTTPException
from pizzaria_api.model.schemas.user_schemas import TokenResponse, UserCreate, UserResponse
from pizzaria_api.model.repository.user_repository import UserRepository
from pizzaria_api.model.entity.models import User
from pizzaria_api.utils.exceptions.object_save_error import ObjectSaveError
from passlib.context import CryptContext
from jose import JWTError, jwt

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "9be5bacc1adb7aaae94a371a4d26a5d1bdbbff51f4e20605c1e1256046c3a268"
ALGORITHM = "HS256"

class UserService:

    def __init__(self, session):
        self.user_repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> UserResponse:

        try:
            new_user = User(
            name_empresa=user_data.name_empresa,
            email=user_data.email,
            password=crypt_context.hash(user_data.password)
        )
            created_user = await self.user_repository.create_user(new_user)
            print(created_user.password)
            return UserResponse(
                name_empresa=created_user.name_empresa,
                email=created_user.email
            )
        except Exception as e:
            raise ObjectSaveError(f"Unable to save the object due to an unexpected error. {e}")

    async def get_user(self, user_id: int) -> UserResponse:
        try:
            user = await self.user_repository.get_user(user_id)
            return UserResponse(
                name_empresa=user.name_empresa,
                email=user.email
            )
        except Exception as e:
            raise Exception(f"Error getting user: {e}")
    
    async def get_all_users(self) -> list[UserResponse]:
        try:
            users = await self.user_repository.get_all_users()
            return [UserResponse(
                name_empresa=user.name_empresa,
                email=user.email
            ) for user in users]
        except Exception as e:
            raise Exception(f"Error getting users: {e}")

    async def update_user(self, user_id: int, user_data: UserCreate) -> UserResponse:
        try:
            user = await self.user_repository.get_user(user_id)
            if not user:
                raise Exception("User not found.")
            user.name_empresa = user_data.name_empresa
            user.email = user_data.email
            user.password = crypt_context.hash(user_data.password)
            updated_user = await self.user_repository.create_user(user)
            return UserResponse(
                name_empresa=updated_user.name_empresa,
                email=updated_user.email
            )
        except Exception as e:
            raise Exception(f"Error updating user: {e}")
        
    async def delete_user(self, user_id: int) -> UserResponse:
        try:
            delete_user = await self.user_repository.delete_user(user_id)
            return UserResponse(
                name_empresa=delete_user.name_empresa,
                email=delete_user.email
            )
        except Exception as e:
            raise Exception(f"Error getting user: {e}")   
        
    async def user_login(self, user: User, expire_in: int = 30) -> TokenResponse:
        user_data = await self.user_repository.get_user_by_email(user.email)

        if not user_data or not crypt_context.verify(user.password, user_data.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        
        exp: int = datetime.utcnow() + timedelta(minutes=expire_in)

        payload = {"sub": user_data.email, "exp": exp}
        acess_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": acess_token, "token_type": "bearer", 'exp': exp.isoformat()}  
    
    async def verify_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_email = payload.get("sub")
            if user_email is None:
                raise HTTPException(status_code=401, detail="Token inválido")
            return user_email  # Retorna o email do usuário ou qualquer outra informação necessária
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        