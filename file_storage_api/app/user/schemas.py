from pydantic import BaseModel, ConfigDict
import uuid


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    password: str


class UserGet(BaseUser):
    id: uuid.UUID
    name: str
    files_count: int
    file_total_size_byte: int


class UserGetList(UserGet):
    name: str
    files_count: int
    file_total_size_byte: int


class UserUpdate(UserCreate):
    pass
