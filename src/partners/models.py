from sqlalchemy import Column, String, Integer

from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base

storage = FileSystemStorage(path="static/media/partners")


class Partners(Base):
    __tablename__ = "partners"

    id: int = Column(Integer, primary_key=True)
    photo: str = Column(FileType(storage=storage), nullable=False)
    link: str = Column(String(500))

    def __repr__(self) -> str:
        return f"{self.link}"
