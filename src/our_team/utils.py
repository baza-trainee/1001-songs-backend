from sqlalchemy.ext.asyncio import AsyncSession
from src.our_team.models import OurTeam

from .exceptions import AFTER_TEAM_CREATE


async def create_fake_team(team_data_list: list[dict], session: AsyncSession):
    from src.utils import write_filetype_field

    field = "photo"
    try:
        write_data_list = []
        for team_data in team_data_list:
            team_data[field] = await write_filetype_field(team_data[field])
            instance = OurTeam(**team_data)
            write_data_list.append(instance)
        session.add_all(write_data_list)
        print(AFTER_TEAM_CREATE)
    except Exception as exc:
        raise exc
