# app/models/base.py

#Inyeccion de dependencias
from fastapi import Depends
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)


from app.config import config


url = URL.create(
    "postgresql+psycopg",
    username=config.db_user,
    password=config.db_password,
    host=config.db_host,
    port=config.db_port,
    database=config.db_name,
)

async_engine = create_async_engine(url)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Necesario para FastAPI para acceder a objetos después del commit
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]