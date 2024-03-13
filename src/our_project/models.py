from sqlalchemy import Column, String, ForeignKey, Integer, Date, ARRAY
from sqlalchemy.orm import relationship
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base


storage = FileSystemStorage(path="static/media/our_projects")


class OurProject(Base):
    __tablename__ = "our_projects"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(60), nullable=False)
    short_description: str = Column(String(200), nullable=False)
    preview_photo: str = Column(FileType(storage=storage), nullable=False)
    project_date = Column(Date, nullable=False)
    content: str = Column(String(10000), nullable=False)
    authors: list[str] = Column(ARRAY(String(25)), nullable=False)
    editors: list[str] = Column(ARRAY(String(25)))
    photographers: list[str] = Column(ARRAY(String(25)))
    city_id = Column(Integer, ForeignKey("cities.id"))
    location = relationship("City", back_populates="projects", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"
