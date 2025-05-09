from fastapi import HTTPException
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from file_storage_api.db.connection import get_db

from fastapi import APIRouter
from fastapi import Depends

from file_storage_api.app.user.schemas import UserGet
from file_storage_api.app.user.schemas import UserGetList
from file_storage_api.app.user.schemas import UserCreate
from file_storage_api.app.user.schemas import UserUpdate
from file_storage_api.app.user.service import UserService

from file_storage_api.config import config
from file_storage_api.app.utils import hash_password, check_hash_password
from file_storage_api.app.security import security, auth_config

router = APIRouter(
        prefix=f"{config.url_prefix}/users"
)


@router.post(
    '', response_model=UserGet, status_code=201
)
async def create_user(
        user_schema: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user_schema.password = hash_password(password=user_schema.password,
                                         username=user_schema.name)
    user = await user_service.create(user_schema)

    return user

@router.post(
    '/login',
)
async def login_user(user_schema: UserCreate,
                     response: Response,
                     db: AsyncSession = Depends(get_db),
                     ):
    user_service = UserService(db)
    user = await user_service.get_by_name(user_schema.name)
    if check_hash_password(user_schema.password,
                           user_schema.name,
                           user.hashed_password):
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return {"response" : "all good"}
    raise HTTPException(status_code=401)



@router.get(
    '', response_model=list[UserGetList]
)
async def get_users(
        db: AsyncSession = Depends(get_db)
):
    user_service: UserService = UserService(db)
    users = await user_service.get_list()

    return users

@router.get(
    '/{name}', response_model=UserGetList
)
async def get_user_by_name(
        name: str,
        db: AsyncSession = Depends(get_db)
):
    user_service: UserService = UserService(db)
    user = await user_service.get_by_name(name=name)

    return user
