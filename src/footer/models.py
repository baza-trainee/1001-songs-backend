from sqlalchemy import Column, String, Integer
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base

storage = FileSystemStorage(path="static/media/footer")


class Footer(Base):
    __tablename__ = "footer"

    id: int = Column(Integer, primary_key=True)
    reporting: str = Column(FileType(storage=storage))
    privacy_policy: str = Column(FileType(storage=storage))
    rules_and_terms: str = Column(FileType(storage=storage))
    email: str = Column(String(length=100))
    facebook_url: str = Column(String(length=500))
    youtube_url: str = Column(String(length=500))
