from sqlalchemy import Column, String, Integer
from src.database.database import Base


class EducationSection(Base):
    __tablename__ = "education_section"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(100), nullable=False)
    description: str = Column(String(5000))
    media1: str = Column(String(500))
    media2: str = Column(String(500))
    media3: str = Column(String(500))
    media4: str = Column(String(500))
    media5: str = Column(String(500))

    @property
    def media(self):
        return [self.media1, self.media2, self.media3, self.media4, self.media5]
