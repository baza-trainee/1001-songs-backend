import os
from uuid import uuid4
import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile
from sqlalchemy import func, select

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
from src.database.fake_data import FAKE_FOOTER, PAYMENT_DATA, FAKE_TEAM, FAKE_EDUCATION


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

    await lock.release()
    yield


async def save_photo(
    file: UploadFile,
    model,
    is_file=False,
) -> str:
    if not is_file and not file.content_type in PHOTO_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
        )
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=OVERSIZE_FILE)
    if is_file and not file.content_type in FILE_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_FILE % (file.content_type, FILE_FORMATS)
        )

    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_name = f'{uuid4().hex}.{file.filename.split(".")[-1]}'
    file_path = os.path.join(folder_path, file_name)

    async def _save_photo(file_path: str):
        os.makedirs(folder_path, exist_ok=True)
        chunk_size = 256
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(chunk_size):
                await buffer.write(chunk)

    await _save_photo(file_path)
    return file_path


async def update_photo(
    file: UploadFile,
    record,
    field_name: str,
    is_file=False,
) -> str:
    old_photo_path = getattr(record, field_name, None)
    new_photo = await save_photo(file, record, is_file)
    if old_photo_path:
        await delete_photo(old_photo_path)
    return new_photo


async def delete_photo(path: str) -> None:
    if "media" in path:
        path_exists = os.path.exists(path)
        if path_exists:
            os.remove(path)
