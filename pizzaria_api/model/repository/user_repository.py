from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession
from pizzaria_api.model.entity.models import User

class UserRepository:
 
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        try:
            async with self.session.begin():
                self.session.add(user) # Adiciona o usuário
                await self.session.flush()  # Garante que o ID seja gerado antes de confirmar
                await self.session.commit()
                return user
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error adding user: {e}")
        finally:
            await self.session.close()

    async def get_user(self, user_id: int) -> User:
        try:
            stmt = select(User).filter(User.pk_id == user_id)
            result = await self.session.execute(stmt)
            user = result.scalars().first()  # Use scalars().first() para obter o primeiro resultado
            return user
        except Exception as e:
            raise Exception(f"Error getting user: {e}")
        finally:
            await self.session.close()

    async def get_all_users(self) -> list[User]:
        try:
            stmt = select(User)
            result = await self.session.execute(stmt) # Executa a consulta no banco de dados e retorna um objeto Result 
            users = result.scalars().all() # Use scalars().all() para obter todos os resultados
            return users
        except Exception as e:
            raise Exception(f"Error getting users: {e}")
        finally:
            await self.session.close()     

    async def delete_user(self, user_id: str) -> User:
        try:
            user = await self.get_user(user_id)
            if not user:
                raise Exception("User not found.")
            await self.session.delete(user) # Deleta o usuário
            await self.session.commit()
            return user
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error deleting user: {e}")
        
    async def get_user_by_email(self, email: str) -> User:
        try:
            stmt = select(User).filter(User.email == email)
            result = await self.session.execute(stmt)
            user = result.scalars().first()
            return user
        except Exception as e:
            raise Exception(f"Error getting user: {e}")
        finally:
            await self.session.close()    