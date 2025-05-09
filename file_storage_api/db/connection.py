from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from file_storage_api.config import config
from contextlib import asynccontextmanager


async_engine = create_async_engine(url=config.DATABASE_URL_ASYNC)


def async_connection() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=async_engine, autocommit=False)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

