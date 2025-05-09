from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from file_storage_api.config import config
from file_storage_api.db.tables import Base, User, File
engine = create_engine(config.DATABASE_URL_SYNC, echo=True)

def create_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(bind=engine)




