from sqlalchemy.ext.asyncio import AsyncSession
from .models import (
    CalendarAndRitualCategory,
    EducationPage,
    EducationPageSongGenre,
    SongSubcategory,
)
from .exceptions import (
    AFTER_EDUCATION_CREATE,
    AFTER_CRC_CREATE,
    AFTER_SUB_CATEGORY_CREATE,
    AFTER_EDUCATION_GENRES_CREATE,
)


async def create_calendar_and_ritual_categories(
    categories: list[dict], session: AsyncSession
):
    try:
        for categoriy in categories:
            instance = CalendarAndRitualCategory(**categoriy)
            session.add(instance)
        print(AFTER_CRC_CREATE)
    except Exception as exc:
        raise exc


async def create_sub_categories(sub_categories: list[dict], session: AsyncSession):
    try:
        for sub_categoriy in sub_categories:
            instance = SongSubcategory(**sub_categoriy)
            session.add(instance)
        print(AFTER_SUB_CATEGORY_CREATE)
    except Exception as exc:
        raise exc


async def create_genres_for_education_page(genres: list[dict], session: AsyncSession):
    try:
        for genre in genres:
            instance = EducationPageSongGenre(**genre)
            session.add(instance)
        print(AFTER_EDUCATION_GENRES_CREATE)
    except Exception as exc:
        raise exc


async def create_education(education_data: dict, session: AsyncSession):
    try:
        instance = EducationPage(**education_data)
        session.add(instance)
        print(AFTER_EDUCATION_CREATE)
    except Exception as exc:
        raise exc
