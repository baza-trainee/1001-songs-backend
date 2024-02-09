from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_FOOTER_CREATE
from .models import Footer


async def create_footer(footer_data: dict, session: AsyncSession):
    try:
        instance = Footer(**footer_data)
        session.add(instance)
        print(AFTER_FOOTER_CREATE)
    except Exception as exc:
        raise exc
