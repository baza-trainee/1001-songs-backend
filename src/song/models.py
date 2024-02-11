from sqlalchemy import Column, String, Date, DateTime, Text, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from src.database.database import Base


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), unique=True)
    recording_date = Column(Date)
    performers = Column(String(200))
    collectors = Column(String(200))
    source = Column(String(200))
    archive = Column(String(255))
    bibliographic_reference = Column(String(1000))
    researcher_comment = Column(String(1000))
    genres = relationship("Genre", secondary="song_genre_association", back_populates="songs")


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(50))
    songs = relationship("Song", secondary="song_genre_association", back_populates="genres")


class SongToGenre(Base):
    __tablename__ = "song_genre_association"

    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)
