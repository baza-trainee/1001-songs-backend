from sqlalchemy import Column, String, Date, DateTime, Text, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base


storage = FileSystemStorage(path="static/media/song")


class Song(Base):
    __tablename__ = "song"

    # MAIN_INFO
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), unique=True)
    song_text = Column(String(2000))
    song_descriotion = Column(String(2000))
    recording_date = Column(Date)
    performers = Column(String(200))
    ethnographic_district = Column(String(100))
    collectors = Column(String(200))
    source = Column(String(200))
    archive = Column(String(255))
    recording_location = Column(String(100))
    bibliographic_reference = Column(String(1000))
    comment_map: str = Column(String(500))

    # MEDIA
    video_url: str = Column(String(1000))
    photo1: str = Column(FileType(storage=storage))
    photo2: str = Column(FileType(storage=storage))
    photo3: str = Column(FileType(storage=storage))
    stereo_audio: str = Column(FileType(storage=storage))
    multichannel_audio1: str = Column(FileType(storage=storage))
    multichannel_audio2: str = Column(FileType(storage=storage))
    multichannel_audio3: str = Column(FileType(storage=storage))
    multichannel_audio4: str = Column(FileType(storage=storage))
    multichannel_audio5: str = Column(FileType(storage=storage))
    multichannel_audio6: str = Column(FileType(storage=storage))

    # RELATIONS
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="songs")
    education_genres = relationship(
        "EducationPageSongGenre",
        secondary="song_education_genre_association",
        back_populates="songs",
    )
    genres = relationship(
        "Genre", secondary="song_genre_association", back_populates="songs"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(100))
    songs = relationship(
        "Song", secondary="song_genre_association", back_populates="genres"
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
