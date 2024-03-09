from sqlalchemy.ext.asyncio import AsyncSession

from .models import Partners
from .exceptions import AFTER_PARTNERS_CREATE


async def create_partners(partners_data: list[dict], session: AsyncSession):
    from src.utils import write_filetype_field

    try:
        field = "photo"
        data_list = []
        for partner in partners_data:
            partner[field] = await write_filetype_field(partner[field], is_file=True)
            instance = Partners(**partner)
            data_list.append(instance)
        session.add_all(data_list)
        print(AFTER_PARTNERS_CREATE)
    except Exception as exc:
        raise exc
