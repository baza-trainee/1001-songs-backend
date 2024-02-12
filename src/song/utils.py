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
    from src.utils import write_filetype_field

    try:
        fields = [
            "stereo_audio",
            "multichannel_audio1",
            "multichannel_audio2",
            "multichannel_audio3",
            "multichannel_audio4",
            "multichannel_audio5",
            "multichannel_audio6",
        ]
        for song in songs_list:
            for field in fields:
                if field in song and song[field]:
                    song[field] = await write_filetype_field(song[field])
            instance = Song(**song)
            session.add(instance)
        print(AFTER_SONG_CREATE)
    except Exception as exc:
        raise exc
