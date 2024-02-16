from sqlalchemy.ext.asyncio import AsyncSession

from .models import Genre, Song, Fund
from .exceptions import AFTER_GENRE_CREATE, AFTER_SONG_CREATE, AFTER_FONDS_CREATE


async def create_genre(genre_list: list[dict], session: AsyncSession):
    try:
        genre_instances = []
        for genre in genre_list:
            instance = Genre(**genre)
            genre_instances.append(instance)
        session.add_all(genre_instances)
        await session.flush()
        print(AFTER_GENRE_CREATE)
        return genre_instances
    except Exception as exc:
        raise exc


async def create_funds(funds_list: list[dict], session: AsyncSession):
    try:
        fund_instances = []
        for fond in funds_list:
            instance = Fund(**fond)
            fund_instances.append(instance)
        session.add_all(fund_instances)
        await session.flush()
        print(AFTER_FONDS_CREATE)
        return fund_instances
    except Exception as exc:
        raise exc


async def create_song_and_genre(
    genre_list: list[dict], songs_list: list[dict], session: AsyncSession
):
    from src.utils import write_filetype_field

    genre_instances = await create_genre(genre_list, session)

    try:
        fields = [
            "photo1",
            "photo2",
            "photo3",
            "map_photo",
            "stereo_audio",
            "multichannel_audio1",
            "multichannel_audio2",
            "multichannel_audio3",
            "multichannel_audio4",
            "multichannel_audio5",
            "multichannel_audio6",
            "ethnographic_photo1",
            "ethnographic_photo2",
            "ethnographic_photo3",
        ]
        song_instances = []
        for song in songs_list:
            for field in fields:
                if field in song and song[field]:
                    song[field] = await write_filetype_field(song[field])
            instance = Song(**song)
            # instance.genres.append(choice(genres))
            song_instances.append(instance)
        session.add_all(song_instances)
        print(AFTER_SONG_CREATE)
    except Exception as exc:
        raise exc
