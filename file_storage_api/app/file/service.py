from fastapi import HTTPException
import uuid
import datetime as dt

from file_storage_api.app.file.schemas import FileGet, FileGetList, FileCreate, \
    FileUpdate
from file_storage_api.db.tables import File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from sqlalchemy import ScalarResult

class FileService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     file_schema: FileCreate,
                     ) -> File:

        file: File = File(**file_schema.model_dump())
        self.session.add(file)
        await self.session.commit()
        await self.session.refresh(file)
        return file

    async def update(self, file_id_: uuid.UUID, file: FileUpdate):
        query = select(File).filter_by(id=file_id_)
        file_update = await self.session.scalar(query)
        if file_update is None:
            raise HTTPException(404)

        updated_file = file.model_dump(exclude_none=True)
        for field, value in updated_file.items():
            setattr(file_update, field, value)

        await self.session.commit()
        return file


    async def get_list(self) -> ScalarResult[File]:
        query = select(File).filter_by(is_available=True)
        files = await self.session.scalars(query)
        return files

    async def get_by_link(self, index_name: str) -> ScalarResult[File]:
        query = select(File).filter_by(index_name=index_name)
        file = await self.session.scalar(query)
        if file is None:
            raise HTTPException(404)
        return file

    async def get(self, user_id_: uuid.UUID) -> ScalarResult[File]:
        query = select(File).filter_by(user_id=user_id_)
        files = await self.session.scalars(query)
        return files

    async def delete(self, id_: uuid.UUID) -> bool:
        query = delete(File).filter_by(id=id_)
        if query is None:
            raise HTTPException(404)
        await self.session.execute(query)
        await self.session.commit()
        return True