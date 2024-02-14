from random import choice

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Genre, Song
from .exceptions import AFTER_GENRE_CREATE, AFTER_SONG_CREATE


async def create_genre(genre_list: list[dict], session: AsyncSession):
    try:
        genre_instances = []
        for genre in genre_list:
            instance = Genre(**genre)
            genre_instances.append(instance)
        await session.flush(genre_instances)
        print(AFTER_GENRE_CREATE)
        return genre_instances
    except Exception as exc:
        raise exc


async def create_song_and_genre(
    genre_list: list[dict], songs_list: list[dict], session: AsyncSession
):
    from src.utils import write_filetype_field

    genre_instances = await create_genre(genre_list, session)
    try:
        fields = [
            "map_photo",
            "stereo_audio",
            "multichannel_audio1",
            "multichannel_audio2",
            "multichannel_audio3",
            "multichannel_audio4",
            "multichannel_audio5",
            "multichannel_audio6",
        ]
        song_instances = []
        for song in songs_list:
            for field in fields:
                if field in song and song[field]:
                    song[field] = await write_filetype_field(song[field])
            instance = Song(**song)
            # instance.genres.append(choice(genre_instances))
            song_instances.append(instance)
        session.add_all(song_instances)
        print(AFTER_SONG_CREATE)
    except Exception as exc:
        raise exc
