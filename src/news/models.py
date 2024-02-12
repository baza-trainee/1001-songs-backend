from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, ARRAY
from sqlalchemy.orm import relationship

from src.database.database import Base


class NewsCategory(Base):
    __tablename__ = "news_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    news = relationship("News", back_populates="category")

    def __repr__(self) -> str:
        return f"{self.name}"


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(String(10000), nullable=False)
    authors = Column(ARRAY(String(100)), nullable=True)
    editors = Column(ARRAY(String(100)), nullable=True)
    photographers = Column(ARRAY(String(100)), nullable=True)
    created_at = Column(DateTime(), nullable=False)
    category_id = Column(Integer, ForeignKey("news_category.id"))

    category = relationship("NewsCategory", back_populates="news")

    def __repr__(self) -> str:
        return f"{self.title}"
