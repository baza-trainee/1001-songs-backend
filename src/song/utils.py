from sqlalchemy.ext.asyncio import AsyncSession
from .models import Genre
from .exceptions import AFTER_GENRE_CREATE


async def create_genre(genre_list: list[dict], session: AsyncSession):
    try:
        for genre in genre_list:
            instance = Genre(**genre)
            session.add(instance)
        print(AFTER_GENRE_CREATE)
    except Exception as exc:
        raise exc
