import base64
import os
import re
from typing import Any
from uuid import uuid4

import aiofiles
from fastapi import FastAPI
from sqlalchemy import func, select
from wtforms import ValidationError

from src.about.utils import create_about
from src.database.database import get_async_session
from src.config import FILE_FORMATS, MAX_FILE_SIZE_MB, PHOTO_FORMATS, settings
from src.database.redis import init_redis, redis
from src.auth.utils import create_user
from src.auth.models import User
from src.exceptions import INVALID_PHOTO, INVALID_FILE, OVERSIZE_FILE
from src.footer.utils import create_footer
from src.our_team.utils import create_fake_team
from src.payment.utils import create_payment
from src.education.utils import create_fake_education
from src.location.utils import create_city, create_countries, create_regions
from src.database.fake_data import (
    FAKE_ABOUT,
    FAKE_FOOTER,
    PAYMENT_DATA,
    FAKE_TEAM,
    FAKE_EDUCATION,
    FAKE_COUNTRIES,
    FAKE_REGIONS,
    FAKE_CITY,
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
                await create_fake_education(FAKE_EDUCATION, s)
                await create_about(FAKE_ABOUT, s)
                await create_countries(FAKE_COUNTRIES, s)
                await create_regions(FAKE_REGIONS, s)
                await create_city(FAKE_CITY, s)

    await lock.release()
    yield


async def save_photo(
    file: str,
    model,
    image_extension: str,
) -> str:
    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_name = f"{uuid4().hex}.{image_extension}"
    file_path = os.path.join(folder_path, file_name)

    async def _save_photo(file_path: str):
        os.makedirs(folder_path, exist_ok=True)
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(file)

    await _save_photo(file_path)
    return file_path


async def delete_photo(path: str) -> None:
    if path and "media" in path:
        path_exists = os.path.exists(path)
        if path_exists:
            os.remove(path)


class MediaValidator:
    def __init__(self, is_file: bool = False) -> None:
        self.is_file = is_file

    def __call__(self, form, field):
        file = field.data
        if file and file.size:
            file_size = round(file.size / 1024 / 1024, 2)
            if file_size > MAX_FILE_SIZE_MB:
                raise ValidationError(
                    message=OVERSIZE_FILE % (file_size, MAX_FILE_SIZE_MB)
                )
            if not self.is_file and not file.content_type in PHOTO_FORMATS:
                raise ValidationError(
                    message=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
                )
            if self.is_file and not file.content_type in FILE_FORMATS:
                raise ValidationError(
                    message=INVALID_FILE % (file.content_type, FILE_FORMATS)
                )


async def model_change_for_editor(data: dict, model: Any, field_name: str):
    pattern_base64 = re.compile(r'(src="data:image/[^;]+;base64,)([^"]+)"')
    matches = pattern_base64.findall(data[field_name])

    for img_data in matches:
        header, base64_string = img_data
        image_extension = header.split("/")[1].split(";")[0]
        image_data = base64.b64decode(base64_string)
        image_path = await save_photo(image_data, model, image_extension)
        image_url = f'<img class="editor-image" src="{settings.BASE_URL}/{image_path}"'
        data[field_name] = re.sub(pattern_base64, image_url, data[field_name], count=1)

    media_folder = model.__tablename__.lower().replace(" ", "_")
    pattern_static = re.compile(f'src="[^"]+(static/media/{media_folder}/[^"]+)"')
    old_data = pattern_static.findall(getattr(model, field_name))
    new_data = pattern_static.findall(data[field_name])
    for file_path in old_data:
        if file_path not in new_data:
            await delete_photo(file_path)
