from fastapi import FastAPI
from file_storage_api.app.user.api import router as user_router
from file_storage_api.app.file.api import router as file_router
from file_storage_api.config import config
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=f'{config.url_prefix}/docs',)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000', 'http://localhost:63342'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user_router)
app.include_router(file_router)


