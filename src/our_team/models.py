from sqlalchemy import Column, String, Integer

from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base

storage = FileSystemStorage(path="static/media/our_team")


class OurTeam(Base):
    __tablename__ = "our_team"

    id: int = Column(Integer, primary_key=True)
    full_name: str = Column(String(100), nullable=False)
    photo: str = Column(FileType(storage=storage))
    description: str = Column(String(500))
