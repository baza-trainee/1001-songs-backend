from sqlalchemy import Column, String, Integer
from src.config import STORAGE
from src.database.database import Base

from fastapi_storages.integrations.sqlalchemy import FileType


class EducationSection(Base):
    __tablename__ = "education_section"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(100), nullable=True)
    description: str = Column(String(5000))
    media1: str = Column(FileType(storage=STORAGE))
    media2: str = Column(FileType(storage=STORAGE))
    media3: str = Column(FileType(storage=STORAGE))
    media4: str = Column(FileType(storage=STORAGE))
    media5: str = Column(FileType(storage=STORAGE))

    @property
    def media(self):
        return [self.media1, self.media2, self.media3, self.media4, self.media5]
