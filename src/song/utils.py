from sqlalchemy.ext.asyncio import AsyncSession
from .models import Genre, Song
from .exceptions import AFTER_GENRE_CREATE, AFTER_SONG_CREATE


async def create_genre(genre_list: list[dict], session: AsyncSession):
    try:
        for genre in genre_list:
            instance = Genre(**genre)
            session.add(instance)
        print(AFTER_GENRE_CREATE)
    except Exception as exc:
        raise exc


async def create_song(songs_list: list[dict], session: AsyncSession):
    try:
        for song in songs_list:
            instance = Song(**song)
            session.add(instance)
        print(AFTER_SONG_CREATE)
    except Exception as exc:
        raise exc
