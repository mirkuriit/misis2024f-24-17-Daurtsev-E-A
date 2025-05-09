from dotenv import load_dotenv
import os


# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)

load_dotenv()

class Config:
    def __init__(
        self,
        POSTGRES_USER: str,
        POSTGRES_PASSWORD: str,
        POSTGRES_PORT: str,
        POSTGRES_HOST: str,
        POSTGRES_DB: str,
        JWT_SECRET_KEY: str,
        JWT_ACCESS_COOKIE_NAME: str,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_endpoint_url: str | None = None,
        aws_bucket_name: str | None = None,
        url_prefix: str = "/file-storage-api",
        file_storage_path: str = "data",

    ):
        self.POSTGRES_PORT = POSTGRES_PORT
        self.POSTGRES_HOST = POSTGRES_HOST
        self.POSTGRES_DB = POSTGRES_DB
        self.POSTGRES_USER = POSTGRES_USER
        self.POSTGRES_PASSWORD = POSTGRES_PASSWORD
        self.AWS_ACCESS_KEY = aws_access_key_id
        self.AWS_SECRET_ACCESS_KEY = aws_secret_access_key
        self.AWS_ENDPOINT_URL = aws_endpoint_url
        self.AWS_BUCKET_NAME = aws_bucket_name
        self.DATABASE_URL_ASYNC=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        self.DATABASE_URL_SYNC=f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        self.url_prefix = url_prefix
        self.file_storage_path = file_storage_path
        self.JWT_SECRET_KEY = JWT_SECRET_KEY
        self.JWT_ACCESS_COOKIE_NAME = JWT_ACCESS_COOKIE_NAME



config = Config(
    POSTGRES_USER=os.getenv("POSTGRES_USER"),
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
    POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
    POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
    POSTGRES_DB=os.getenv("POSTGRES_DB"),
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    JWT_ACCESS_COOKIE_NAME=os.getenv("JWT_ACCESS_COOKIE_NAME")
)

print(os.path.isdir(config.file_storage_path))
