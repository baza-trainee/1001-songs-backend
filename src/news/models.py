from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer, Date, ARRAY
from sqlalchemy.orm import relationship

from src.database.database import Base


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
    location: str = Column(String(100), nullable=False)
    created_at: datetime = Column(Date(), nullable=False)
    category_id: int = Column(Integer, ForeignKey("news_category.id"))

    category = relationship("NewsCategory", back_populates="news")

    def __repr__(self) -> str:
        return f"{self.title}"
