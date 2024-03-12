from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer
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
    title: str = Column(String(70), nullable=False)
    description: str = Column(String(600), nullable=False)
    recommendations: str = Column(String(10000), nullable=False)
    recommended_sources: str = Column(String(10000), nullable=False)


class CalendarAndRitualCategory(Base):
    __tablename__ = "calendar_and_ritual_categories"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(50), nullable=False)
    media = Column(FileType(storage=storage1), nullable=False)
    description: str = Column(String(2000), nullable=False)
    recommended_sources: str = Column(String(10000), nullable=False)

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

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(70), nullable=False)
    media = Column(FileType(storage=storage2), nullable=False)
    main_category_id: int = Column(
        Integer, ForeignKey("calendar_and_ritual_categories.id")
    )

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

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(70), nullable=False)
    description: str = Column(String(2000), nullable=False)
    media1: str = Column(FileType(storage=storage3), nullable=False)
    media2: str = Column(FileType(storage=storage3), nullable=False)
    media3: str = Column(FileType(storage=storage3), nullable=False)
    media4: str = Column(FileType(storage=storage3))
    media5: str = Column(FileType(storage=storage3))
    main_category_id: int = Column(
        Integer, ForeignKey("calendar_and_ritual_categories.id")
    )
    sub_category_id: int = Column(Integer, ForeignKey("song_subcategories.id"))

    main_category = relationship(
        "CalendarAndRitualCategory",
        back_populates="education_genres",
        lazy="selectin",
    )
    sub_category = relationship(
        "SongSubcategory",
        back_populates="education_genres",
        lazy="selectin",
    )
    songs = relationship(
        "Song",
        secondary="song_education_genre_association",
        back_populates="education_genres",
        lazy="selectin",
    )

    @property
    def media(self):
        return [self.media1, self.media2, self.media3, self.media4, self.media5]

    def __repr__(self) -> str:
        return f"{self.title}"
