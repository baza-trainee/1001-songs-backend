from sqlalchemy import Column, String, ForeignKey, Integer, Date, ARRAY
from sqlalchemy.orm import relationship
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base


storage = FileSystemStorage(path="static/media/expedition")


class ExpeditionCategory(Base):
    __tablename__ = "expedition_category"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=30))
    expeditions = relationship("Expedition", back_populates="category", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"


class Expedition(Base):
    __tablename__ = "expedition"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(250), nullable=False)
    short_description: str = Column(String(120), nullable=False)
    map_photo: str = Column(FileType(storage=storage))
    preview_photo: str = Column(FileType(storage=storage))
    expedition_date = Column(Date)
    content: str = Column(String(10000), nullable=False)
    category_id = Column(Integer, ForeignKey("expedition_category.id"))
    category = relationship(
        "ExpeditionCategory", back_populates="expeditions", lazy="selectin"
    )

    city_id = Column(Integer, ForeignKey("cities.id"))
    location = relationship("City", back_populates="expeditions", lazy="selectin")

    authors: list[str] = Column(ARRAY(String(100)), nullable=True)
    editors: list[str] = Column(ARRAY(String(100)), nullable=True)
    photographers: list[str] = Column(ARRAY(String(100)), nullable=True)
    recording: list[str] = Column(ARRAY(String(100)), nullable=True)

    def __repr__(self) -> str:
        return f"{self.title}"
