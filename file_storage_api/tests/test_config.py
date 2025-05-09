import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from file_storage_api.config import config
from file_storage_api.db.connection import get_db
from file_storage_api.app.security import security, auth_config

def test_security_config():
    assert config.JWT_SECRET_KEY is not None
    assert config.JWT_ACCESS_COOKIE_NAME is not None
    assert isinstance(config.JWT_SECRET_KEY, str)
    assert isinstance(config.JWT_ACCESS_COOKIE_NAME, str)
    assert auth_config.JWT_SECRET_KEY == config.JWT_SECRET_KEY
    assert auth_config.JWT_ACCESS_COOKIE_NAME == config.JWT_ACCESS_COOKIE_NAME
    assert auth_config.JWT_TOKEN_LOCATION == ["cookies"]

def test_database_config():
    assert config.POSTGRES_USER is not None
    assert config.POSTGRES_PASSWORD is not None
    assert config.POSTGRES_HOST is not None
    assert config.POSTGRES_PORT is not None
    assert config.POSTGRES_DB is not None
    assert "postgresql+asyncpg://" in config.DATABASE_URL_ASYNC
    assert "postgresql+psycopg://" in config.DATABASE_URL_SYNC

@pytest.mark.asyncio
async def test_database_connection():
    async for session in get_db():
        assert isinstance(session, AsyncSession)
        try:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
            break
        except Exception as e:
            pytest.fail(f"Database connection failed: {str(e)}") 