import asyncio
from io import BytesIO
import os
from uuid import uuid4

import aiofiles
from fastapi import FastAPI, UploadFile
from sqlalchemy import func, select

from src.about.utils import create_about
from src.database.database import get_async_session
from src.config import settings
from src.database.redis import init_redis, redis
from src.auth.utils import create_user
from src.auth.models import User
from src.footer.utils import create_footer
from src.news.utils import create_news, create_news_category
from src.our_team.utils import create_fake_team
from src.partners.utils import create_partners
from src.payment.utils import create_payment
from src.education.utils import (
    create_calendar_and_ritual_categories,
    create_sub_categories,
    create_genres_for_education_page,
    create_education,
)
from src.location.utils import create_city, create_countries, create_regions
from src.expedition.utils import create_expedition_categories, create_expeditions
from src.song.utils import create_song_and_genre, create_funds
from src.our_project.utils import create_projects
from src.database.fake_data import (
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
    PARTNERS,
)


lock = redis.lock("my_lock")


async def lifespan(app: FastAPI):
    await init_redis()
    await lock.acquire(blocking=True)
    async for s in get_async_session():
        async with s.begin():
            user_count = await s.scalar(select(func.count()).select_from(User))
            if user_count == 0:
                await create_user(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD)
                await create_payment(PAYMENT_DATA, s)
                await create_fake_team(FAKE_TEAM, s)
                await create_footer(FAKE_FOOTER, s)
                await create_calendar_and_ritual_categories(ES_MAIN_SONG_CATEGORY, s)
                await create_about(FAKE_ABOUT, s)
                await create_countries(FAKE_COUNTRIES, s)
                await create_regions(FAKE_REGIONS, s)
                await create_city(FAKE_CITY, s)
                await create_song_and_genre(FAKE_GENRE, FAKE_SONG, s)
                await create_sub_categories(FAKE_SUB_CATEGORY, s)
                await create_genres_for_education_page(FAKE_GENRE_ES, s)
                await create_education(FAKE_EDUCATION, s)
                await create_news_category(FAKE_NEWS_CATEGORY, s)
                await create_news(FAKE_NEWS, s)
                await create_expedition_categories(FAKE_EXPED_CATEGORY, s)
                await create_expeditions(FAKE_EXPEDITIONS, s)
                await create_projects(FAKE_PROJECTS, s)
                await create_funds(FAKE_FUNDS, s)
                await create_partners(PARTNERS, s)
    await lock.release()
    yield


def save_photo(
    file: str,
    model,
    image_extension: str,
) -> str:
    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_name = generate_file_name(image_extension=image_extension)
    file_path = os.path.join(folder_path, file_name)

    async def _save_photo(file_path: str):
        os.makedirs(folder_path, exist_ok=True)
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(file)

    loop = asyncio.get_event_loop()
    loop.create_task(_save_photo(file_path))
    return file_path


def generate_file_name(filepath: str = None, image_extension: str = None):
    "file or image_extension with <.>"
    name = uuid4().hex
    if not image_extension:
        image_extension = "." + filepath.split("/")[-1].split(".")[-1]
    return name + image_extension


async def write_filetype_field(file_path: str) -> UploadFile:
    async with aiofiles.open(file_path, "rb") as buffer:
        file_name = generate_file_name(file_path)
        return UploadFile(file=BytesIO(await buffer.read()), filename=file_name)


def delete_photo(path: str) -> None:
    async def _delete_photo(path):
        if path and "media" in path:
            path_exists = os.path.exists(path)
            if path_exists:
                os.remove(path)

    loop = asyncio.get_event_loop()
    loop.create_task(_delete_photo(path))
