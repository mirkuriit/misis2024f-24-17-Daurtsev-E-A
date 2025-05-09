import datetime as dt
import uuid
from email.policy import default

from sqlalchemy.dialects.postgresql import UUID

from pydantic import EmailStr
from sqlalchemy.orm import mapped_column as column
from sqlalchemy import text
from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: M[uuid.UUID] = column(
        primary_key=True,
        server_default=text('gen_random_uuid()')
    )

    name: M[str] = column(nullable=False)
    hashed_password: M[str] = column(nullable=False)
    files: M["File"] = relationship(back_populates="user",
                                    lazy="selectin",
                                    cascade="all, delete")
    files_count: M[int] = column(default=0)
    file_total_size_byte: M[int] = column(default=0)

    created_at: M[dt.datetime] = column(server_default=func.now())
    updated_at: M[dt.datetime] = column(
        server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"hashed_password='{self.hashed_password}', "
            f"files_count={self.files_count}, "
            f"file_total_size_byte={self.file_total_size_byte}, "
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at}"
            f")"
        )


class File(Base):
    __tablename__ = "files"

    id: M[uuid.UUID] = column(
        primary_key=True,
        server_default=text('gen_random_uuid()'),
    )
    user_id: M[uuid.UUID] = column(ForeignKey("users.id", ondelete="CASCADE"))
    user: M["User"] = relationship(back_populates="files", lazy="selectin")
    bytesize: M[int] = column(nullable=False)
    name: M[str] = column(nullable=False)
    index_name: M[str] = column(nullable=False)
    link: M[str] = column(nullable=False)
    is_available: M[bool] = column(default=True)
    live_time: M[dt.timedelta] = column(server_default=None)
    path: M[str] = column(nullable=False)

    created_at: M[dt.datetime] = column(server_default=func.now())
    updated_at: M[dt.datetime] = column(
        server_default=func.now(), onupdate=func.now()
    )
