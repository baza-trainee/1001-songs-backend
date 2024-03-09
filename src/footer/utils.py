from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import AFTER_FOOTER_CREATE
from .models import Footer


async def create_footer(footer_data: dict, session: AsyncSession):
    from src.utils import write_filetype_field

    try:
        fields = ["privacy_policy", "reporting", "rules_and_terms"]
        for field in fields:
            footer_data[field] = await write_filetype_field(
                footer_data[field], is_file=True
            )
        instance = Footer(**footer_data)
        session.add(instance)
        print(AFTER_FOOTER_CREATE)
    except Exception as exc:
        raise exc
