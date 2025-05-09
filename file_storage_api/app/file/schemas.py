from pydantic import BaseModel, ConfigDict
import uuid
import datetime as dt

class BaseFile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class FileCreate(BaseFile):
    user_id: uuid.UUID
    name: str
    is_available: bool = True
    live_time: dt.timedelta
    bytesize: int
    index_name: str
    link: str
    path: str


class FileGet(BaseFile):
    id: uuid.UUID
    user_id: uuid.UUID
    bytesize: int
    name: str
    link: str
    is_available: bool = True
    live_time: dt.timedelta


class FileGetList(FileGet):
    created_at: dt.datetime


class FileUpdate(BaseFile):
    bytesize: int
    name: str
    link: str
    is_available: bool = True
    live_time: dt.timedelta