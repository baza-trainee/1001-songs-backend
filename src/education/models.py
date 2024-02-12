from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base


storage1 = FileSystemStorage(path="static/media/calendar_and_ritual_categories")
storage2 = FileSystemStorage(path="static/media/song_subcategories")
storage3 = FileSystemStorage(path="static/media/education_page_song_genres")


class EducationPage(Base):
    __tablename__ = "education_page"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(100), nullable=True)
    description: str = Column(String(5000))
    recommendations: str = Column(String(10000))
    recommended_sources: str = Column(String(10000))


class CalendarAndRitualCategory(Base):
    __tablename__ = "calendar_and_ritual_categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    media = Column(FileType(storage=storage1))
    description = Column(String(2000))
    recommended_sources = Column(String(10000))

    song_subcategories = relationship(
        "SongSubcategory", back_populates="main_category", lazy="selectin"
    )
    education_genres = relationship(
        "EducationPageSongGenre", back_populates="main_category"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class SongSubcategory(Base):
    __tablename__ = "song_subcategories"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    media = Column(FileType(storage=storage2))
    main_category_id = Column(Integer, ForeignKey("calendar_and_ritual_categories.id"))

    main_category = relationship(
        "CalendarAndRitualCategory", back_populates="song_subcategories"
    )
    education_genres = relationship(
        "EducationPageSongGenre", back_populates="sub_category", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class EducationPageSongGenre(Base):
    __tablename__ = "education_page_song_genres"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(2000))
    media1: str = Column(FileType(storage=storage3))
    media2: str = Column(FileType(storage=storage3))
    media3: str = Column(FileType(storage=storage3))
    media4: str = Column(FileType(storage=storage3))
    media5: str = Column(FileType(storage=storage3))
    main_category_id = Column(Integer, ForeignKey("calendar_and_ritual_categories.id"))
    sub_category_id = Column(Integer, ForeignKey("song_subcategories.id"))

    main_category = relationship(
        "CalendarAndRitualCategory", back_populates="education_genres"
    )
    sub_category = relationship("SongSubcategory", back_populates="education_genres")
    songs = relationship(
        "Song",
        secondary="song_education_genre_association",
        back_populates="education_genres",
    )

    @property
    def media(self):
        return [self.media1, self.media2, self.media3, self.media4, self.media5]

    def __repr__(self) -> str:
        return f"{self.title}"
