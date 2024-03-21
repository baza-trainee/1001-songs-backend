from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_ABOUT_CREATE
from .models import About


async def create_about(hero_data: dict, session: AsyncSession):
    try:
        instance = About(**hero_data)
        session.add(instance)
        print(AFTER_ABOUT_CREATE)
    except Exception as exc:
        raise exc
