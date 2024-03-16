from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    String,
    Date,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base


storage = FileSystemStorage(path="static/media/song")


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), nullable=False)
    song_text = Column(String(5000))
    song_description = Column(String(200))
    recording_date = Column(Date, nullable=False)
    performers = Column(String(200), nullable=False)
    ethnographic_district = Column(String(50), nullable=False)
    collectors: list[str] = Column(ARRAY(String(25)), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    video_url: str = Column(String(500))
    map_photo: str = Column(FileType(storage=storage))
    comment_map: str = Column(String(200))
    photo1: str = Column(FileType(storage=storage), nullable=False)
    photo2: str = Column(FileType(storage=storage))
    photo3: str = Column(FileType(storage=storage))
    photo4: str = Column(FileType(storage=storage))
    photo5: str = Column(FileType(storage=storage))
    ethnographic_photo1: str = Column(FileType(storage=storage), nullable=False)
    ethnographic_photo2: str = Column(FileType(storage=storage))
    ethnographic_photo3: str = Column(FileType(storage=storage))
    ethnographic_photo4: str = Column(FileType(storage=storage))
    ethnographic_photo5: str = Column(FileType(storage=storage))
    stereo_audio: str = Column(FileType(storage=storage))
    multichannel_audio1: str = Column(FileType(storage=storage))
    multichannel_audio2: str = Column(FileType(storage=storage))
    multichannel_audio3: str = Column(FileType(storage=storage))
    multichannel_audio4: str = Column(FileType(storage=storage))
    multichannel_audio5: str = Column(FileType(storage=storage))
    multichannel_audio6: str = Column(FileType(storage=storage))
    fund_id = Column(Integer, ForeignKey("funds.id"))
    fund = relationship("Fund", back_populates="songs", lazy="selectin")
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship(
        "City",
        back_populates="songs",
        lazy="selectin",
    )
    education_genres = relationship(
        "EducationPageSongGenre",
        secondary="song_education_genre_association",
        back_populates="songs",
        lazy="selectin",
    )
    genres = relationship(
        "Genre",
        secondary="song_genre_association",
        back_populates="songs",
        lazy="selectin",
    )

    @property
    def photos(self):
        return [
            self.photo1,
            self.photo2,
            self.photo3,
            self.photo4,
            self.photo5,
        ]

    @property
    def ethnographic_photos(self):
        return [
            self.ethnographic_photo1,
            self.ethnographic_photo2,
            self.ethnographic_photo3,
            self.ethnographic_photo4,
            self.ethnographic_photo5,
        ]

    @property
    def multichannels(self):
        return [
            self.multichannel_audio1,
            self.multichannel_audio2,
            self.multichannel_audio3,
            self.multichannel_audio4,
            self.multichannel_audio5,
            self.multichannel_audio6,
        ]

    def __repr__(self) -> str:
        return f"{self.title}"


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(50), nullable=False)
    songs = relationship(
        "Song",
        secondary="song_genre_association",
        back_populates="genres",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"{self.genre_name}"


class SongToGenre(Base):
    __tablename__ = "song_genre_association"

    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)


class SongToEducationGenre(Base):
    __tablename__ = "song_education_genre_association"

    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    education_genre_id = Column(
        Integer, ForeignKey("education_page_song_genres.id"), primary_key=True
    )


class Fund(Base):
    __tablename__ = "funds"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)

    songs = relationship("Song", back_populates="fund", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.title}"
