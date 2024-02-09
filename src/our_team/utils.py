from sqlalchemy.ext.asyncio import AsyncSession
from src.our_team.models import OurTeam
from .exceptions import AFTER_TEAM_CREATE


async def create_fake_team(team_data_list: list[dict], session: AsyncSession):
    try:
        for team_data in team_data_list:
            instance = OurTeam(**team_data)
            session.add(instance)
        print(AFTER_TEAM_CREATE)
    except Exception as exc:
        raise exc
