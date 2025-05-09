import uuid
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi import UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.responses import FileResponse

import datetime as dt

from file_storage_api.db.connection import get_db
from file_storage_api.app.file.schemas import FileCreate, FileUpdate, FileGet, \
    FileGetList
from file_storage_api.app.file.service import FileService
from file_storage_api.config import config

from typing import List
from file_storage_api.config import config
from file_storage_api.app.security import security


router = APIRouter(
    prefix=f"{config.url_prefix}/files",
    tags=["files"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_file(
        user_id: uuid.UUID = Form(...),
        is_available: bool = Form(...),
        live_time: dt.timedelta = Form(),
        file_upload: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),

):
    print(file_upload)
    file_service = FileService(db)
    file_path = f"{os.path.join(config.file_storage_path, str(user_id)) + '.' + file_upload.filename}"
    index_name = f"{str(user_id) + '.' + file_upload.filename}"

    file_schema: FileCreate = FileCreate(
        user_id=user_id,
        is_available=is_available,
        name=file_upload.filename,
        live_time=live_time,
        bytesize=file_upload.size,
        index_name=index_name,
        ### TODO харк код
        link=f"{os.path.join('http://0.0.0.0:8000/file-storage-api/files', index_name)}",
        path=file_path
    )

    print(file_path)
    with open(file_path, "wb") as f:
        f.write(file_upload.file.read())
    file = await file_service.create(
        file_schema=file_schema,
    )
    return file


@router.get(
    "",
    response_model=List[FileGetList],
    dependencies=[Depends(security.access_token_required)]
)
async def get_files(
        db: AsyncSession = Depends(get_db)
):
    file_service = FileService(db)

    files = await file_service.get_list()
    return list(files)


@router.get(
    "/{index_name}",
)
async def download_file_by_link(
        index_name: str,
        db: AsyncSession = Depends(get_db)
        ):
    file_service = FileService(db)
    file = await file_service.get_by_link(index_name)
    print(file.path, file)
    return FileResponse(
        path=file.path,
        headers={f"Content-Disposition": f"attachment; filename={file.name}"}
    )



@router.get(
    "/user/{user_id}",
    response_model=List[FileGetList],
    dependencies=[Depends(security.access_token_required)]
)
async def get_files_by_user(
        user_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    file_service = FileService(db)
    files = list(await file_service.get(user_id))
    response_files: list[FileGetList] = []
    for i in range(len(files)):
        file = files[i]
        created_time = file.created_at
        live_time = file.live_time
        if created_time + live_time < dt.datetime.now():
            await file_service.delete(file.id)
        else:
            response_files.append(file)

    return list(files)


@router.put(
    "/{file_id}",
    response_model=FileUpdate
)
async def update_file(
        file_id: uuid.UUID,
        file_data: FileUpdate,
        db: AsyncSession = Depends(get_db)
):
    file_service = FileService(db)
    file = await file_service.update(file_id, file_data)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.delete(
    "/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_file(
        file_id: uuid.UUID,
        db: AsyncSession = Depends(get_db)
):
    file_service = FileService(db)
    deleted = await file_service.delete(file_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="File not found")
