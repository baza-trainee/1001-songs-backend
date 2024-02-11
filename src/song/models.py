from sqlalchemy import Column, String, Date, DateTime, Text, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from src.database.database import Base


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
    photo1: str = Column(String(500))
    photo2: str = Column(String(500))
    photo3: str = Column(String(500))
    stereo_audio: str = Column(String(1000))
    multichannel_audio1: str = Column(String(1000))
    multichannel_audio2: str = Column(String(1000))
    multichannel_audio3: str = Column(String(1000))
    multichannel_audio4: str = Column(String(1000))
    multichannel_audio5: str = Column(String(1000))
    multichannel_audio6: str = Column(String(1000))

    # RELATIONS
    city_id = Column(Integer, ForeignKey("cities.id"))
    city = relationship("City", back_populates="songs")
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
