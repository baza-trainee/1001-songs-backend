from sqlalchemy import Column, String, Integer

from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base

storage = FileSystemStorage(path="static/media/our_team")


class OurTeam(Base):
    __tablename__ = "our_team"

    id: int = Column(Integer, primary_key=True)
    full_name: str = Column(String(50), nullable=False)
    photo: str = Column(FileType(storage=storage), nullable=False)
    description: str = Column(String(300), nullable=False)

    def __repr__(self) -> str:
        return f"{self.full_name}"
