from datetime import datetime
from fastapi_storages import FileSystemStorage
from sqlalchemy import Column, String, ForeignKey, Integer, Date, ARRAY
from sqlalchemy.orm import relationship
from fastapi_storages.integrations.sqlalchemy import FileType

from src.database.database import Base

storage = FileSystemStorage(path="static/media/news")


class NewsCategory(Base):
    __tablename__ = "news_category"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)

    news = relationship("News", back_populates="category")

    def __repr__(self) -> str:
        return f"{self.name}"


class News(Base):
    __tablename__ = "news"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(250), nullable=False)
    content: str = Column(String(10000), nullable=False)
    slider_caption: str = Column(String(100), nullable=True)
    authors: list[str] = Column(ARRAY(String(100)), nullable=True)
    editors: list[str] = Column(ARRAY(String(100)), nullable=True)
    photographers: list[str] = Column(ARRAY(String(100)), nullable=True)
    preview_photo: str = Column(FileType(storage=storage))
    created_at: datetime = Column(Date(), nullable=False)
    category_id: int = Column(Integer, ForeignKey("news_category.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))

    category = relationship("NewsCategory", back_populates="news", lazy="selectin")
    location = relationship("City", back_populates="news", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"
