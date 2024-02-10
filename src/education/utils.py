from sqlalchemy.ext.asyncio import AsyncSession
from .models import EducationSection
from .exceptions import AFTER_EDUCATION_CREATE


async def create_fake_education(education_data: list[dict], session: AsyncSession):
    try:
        for team_data in education_data:
            instance = EducationSection(**team_data)
            session.add(instance)
        print(AFTER_EDUCATION_CREATE)
    except Exception as exc:
        raise exc
