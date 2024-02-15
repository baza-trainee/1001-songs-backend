from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_CATEGORY_CREATE
from .models import ExpeditionCategory


async def create_expedition_categories(categories: list[dict], session: AsyncSession):
    try:
        for category in categories:
            instance = ExpeditionCategory(**category)
            session.add(instance)
        print(AFTER_CATEGORY_CREATE)
    except Exception as exc:
        raise exc
