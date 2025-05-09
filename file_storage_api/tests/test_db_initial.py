import pytest
from sqlalchemy import inspect
from file_storage_api.db.initial import create_db, drop_db
from file_storage_api.db.tables import Base, User, File
from file_storage_api.db.connection import async_engine

@pytest.mark.asyncio
async def test_database_initialization():
    """Test database initialization and table creation"""
    drop_db()
    create_db()
    
    async with async_engine.connect() as conn:
        tables = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())
        
        assert "users" in tables
        assert "files" in tables
        
        user_columns = await conn.run_sync(
            lambda sync_conn: {col['name'] for col in inspect(sync_conn).get_columns('users')}
        )
        expected_user_columns = {
            'id', 'name', 'hashed_password', 'files_count',
            'file_total_size_byte', 'created_at', 'updated_at'
        }
        assert expected_user_columns.issubset(user_columns)
        
        file_columns = await conn.run_sync(
            lambda sync_conn: {col['name'] for col in inspect(sync_conn).get_columns('files')}
        )
        expected_file_columns = {
            'id', 'user_id', 'bytesize', 'name', 'index_name',
            'link', 'is_available', 'live_time', 'path',
            'created_at', 'updated_at'
        }
        assert expected_file_columns.issubset(file_columns)
        
        foreign_keys = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_foreign_keys('files')
        )
        assert any(fk['referred_table'] == 'users' for fk in foreign_keys)
    
    drop_db()
    
    async with async_engine.connect() as conn:
        tables_after_drop = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )
        assert "users" not in tables_after_drop
        assert "files" not in tables_after_drop 