import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def pytest_configure(config):
    required_vars = [
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "JWT_SECRET_KEY",
        "JWT_ACCESS_COOKIE_NAME"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        pytest.fail(f"Missing required environment variables: {', '.join(missing_vars)}") 