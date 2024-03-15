import asyncio
from random import choice
from typing import Any

from sqlalchemy import func, select

from src.about.models import About
from src.admin.commons.exceptions import AFTER_MODEL_CREATE
from src.auth.models import User
from src.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import async_session_maker
from scripts.fake_data import (
    FAKE_ABOUT,
    FAKE_FOOTER,
    FAKE_NEWS,
    FAKE_NEWS_CATEGORY,
    PAYMENT_DATA,
    FAKE_TEAM,
    FAKE_EDUCATION,
    FAKE_COUNTRIES,
    FAKE_REGIONS,
    FAKE_CITY,
    FAKE_GENRE,
    FAKE_GENRE_ES,
    FAKE_SONG,
    ES_MAIN_SONG_CATEGORY,
    FAKE_SUB_CATEGORY,
    FAKE_EXPED_CATEGORY,
    FAKE_PROJECTS,
    FAKE_EXPEDITIONS,
    FAKE_FUNDS,
    FAKE_PARTNERS,
    FAKE_EXPEDITION_ABOUT,
)
from src.auth.utils import add_user_data
from src.education.models import (
    CalendarAndRitualCategory,
    EducationPage,
    EducationPageSongGenre,
    SongSubcategory,
)
from src.expedition.models import Expedition, ExpeditionCategory, ExpeditionInfo
from src.footer.models import Footer
from src.location.models import City, Country, Region
from src.news.models import News, NewsCategory
from src.our_project.models import OurProject
from src.our_team.models import OurTeam
from src.partners.models import Partners
from src.payment.models import PaymentDetails
from src.song.models import Fund, Genre, Song

fake_data = [
    {"data": FAKE_ABOUT, "model": About},
    {"data": FAKE_FOOTER, "model": Footer},
    {"data": FAKE_NEWS, "model": News},
    {"data": FAKE_NEWS_CATEGORY, "model": NewsCategory},
    {"data": PAYMENT_DATA, "model": PaymentDetails},
    {"data": FAKE_TEAM, "model": OurTeam},
    {"data": FAKE_EDUCATION, "model": EducationPage},
    {"data": FAKE_COUNTRIES, "model": Country},
    {"data": FAKE_REGIONS, "model": Region},
    {"data": FAKE_CITY, "model": City},
    {"data": FAKE_GENRE_ES, "model": EducationPageSongGenre},
    {"data": ES_MAIN_SONG_CATEGORY, "model": CalendarAndRitualCategory},
    {"data": FAKE_SUB_CATEGORY, "model": SongSubcategory},
    {"data": FAKE_EXPED_CATEGORY, "model": ExpeditionCategory},
    {"data": FAKE_PROJECTS, "model": OurProject},
    {"data": FAKE_EXPEDITIONS, "model": Expedition},
    {"data": FAKE_FUNDS, "model": Fund},
    {"data": FAKE_PARTNERS, "model": Partners},
    {"data": FAKE_EXPEDITION_ABOUT, "model": ExpeditionInfo},
]


def add_instances(model: Any, data: dict | list, session: AsyncSession):
    try:
        instances_list = []
        if isinstance(data, dict):
            data = [data]
        for item_data in data:
            instance = model(**item_data)
            instances_list.append(instance)
        session.add_all(instances_list)
        print(AFTER_MODEL_CREATE % model.__tablename__)
        return instances_list
    except Exception as exc:
        raise exc


async def create_initial_data():
    async with async_session_maker() as s:
        user_count = await s.scalar(select(func.count()).select_from(User))
        if user_count == 0:
            add_user_data(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD, s)

            for initial_data in fake_data:
                add_instances(**initial_data, session=s)

            genre_instances = add_instances(model=Genre, data=FAKE_GENRE, session=s)
            await s.flush()
            song_instances = add_instances(model=Song, data=FAKE_SONG, session=s)
            for song_instance in song_instances:
                song_instance.genres.append(choice(genre_instances))

            await s.commit()


if __name__ == "__main__":
    asyncio.run(create_initial_data())
