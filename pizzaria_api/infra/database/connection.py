# São responsáveis por criar a conexão com o banco de dados e a sessão com o banco de dados
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# Responsavel por criar uma sessão com o banco de dados
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco de dados
DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost/pizzaria_api"

# Cria a sessão com o banco de dados
engine = create_async_engine(DATABASE_URL, echo=True)

# Para dizer que a sessão é assíncrona 
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Metodo para retornar a sessão 
async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session