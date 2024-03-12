from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import (
    AFTER_CATEGORY_CREATE,
    AFTER_EXPEDITION_CREATE,
    AFTER_INFO_CREATE,
)
from .models import ExpeditionCategory, Expedition, ExpeditionInfo


async def create_expedition_categories(categories: list[dict], session: AsyncSession):
    try:
        for category in categories:
            instance = ExpeditionCategory(**category)
            session.add(instance)
        print(AFTER_CATEGORY_CREATE)
    except Exception as exc:
        raise exc


async def create_expedition_info(info: dict, session: AsyncSession):
    try:
        session.add(ExpeditionInfo(**info))
        print(AFTER_INFO_CREATE)
    except Exception as exc:
        raise exc


async def create_expeditions(expeditions_list: list[dict], session: AsyncSession):
    from src.utils import write_filetype_field

    try:
        add_data = []
        for expedition in expeditions_list:
            fields = ["preview_photo", "map_photo"]
            for field in fields:
                if expedition[field]:
                    expedition[field] = await write_filetype_field(expedition[field])
            instance = Expedition(**expedition)
            add_data.append(instance)
        session.add_all(add_data)
        print(AFTER_EXPEDITION_CREATE)
    except Exception as exc:
        raise exc
