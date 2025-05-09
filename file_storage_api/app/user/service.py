from fastapi import HTTPException
from sqlalchemy import ScalarResult

from sqlalchemy.ext.asyncio import AsyncSession

from file_storage_api.app.user.schemas import UserCreate, UserGet, UserGetList, \
    UserUpdate
from file_storage_api.db.tables import User, File

from sqlalchemy import select, delete

import uuid


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_schema: UserCreate) -> User:
        user = User(**user_schema.model_dump(exclude={"password"}))
        user.hashed_password = user_schema.password

        self.session.add(user)
        print(user)
        await self.session.commit()
        await self.session.refresh(user)
        print(user)
        return user

    async def get_by_id(self, id_: uuid.UUID) -> User:
        query = select(User).filter_by(id=id_)
        # user_scalar = a | Nonewait self.session.scalar(query)
        user_execute = await self.session.execute(query)
        return user_execute.scalar()

    async def get_by_name(self, name: str) -> User:
        query = select(User).filter_by(name=name)
        user_execute = await self.session.execute(query)
        return user_execute.scalar()

    async def get_list(self) -> ScalarResult[User]:
        query = select(User)
        # user_scalar = a | Nonewait self.session.scalar(query)
        user_execute = await self.session.execute(query)
        return user_execute.scalars()

    async def get_by_name(self, name: str) -> User:
        query = select(User).filter_by(name=name)
        # user_scalar = await self.session.scalar(query)
        user_execute = await self.session.execute(query)
        return user_execute.scalar()

    async def delete_by_id(self, id_: uuid.UUID) -> UserGet:
        query = select(User).filter_by(id=id_)
        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(404)
        await self.session.delete(user)
        await self.session.commit()
        return user

    async def update(self, id_: uuid.UUID, user_update: UserUpdate) -> User:
        query = select(User).filter_by(id=id_)
        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(404)

        updated_user = user_update.model_dump(exclude_none=True)
        for field, value in updated_user.items():
            setattr(user, field, value)

        await self.session.commit()

        return user
