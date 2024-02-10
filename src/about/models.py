from sqlalchemy import Column, Integer, String

from src.database.database import Base


class About(Base):
    __tablename__ = "about"

    id: int = Column(Integer, primary_key=True)
    content: str = Column(String(length=10000), nullable=False)
