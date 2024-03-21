import asyncio
from io import BytesIO
import os
from uuid import uuid4

import aiofiles
from fastapi import FastAPI, UploadFile
from fastapi_limiter import FastAPILimiter

from src.database.redis import init_redis


async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await FastAPILimiter.close()


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


def create_file_field(file_path: str) -> UploadFile:
    file_name = generate_file_name(file_path)
    with open(file_path, "rb") as buffer:
        file_bytes = buffer.read()
    return UploadFile(file=BytesIO(file_bytes), filename=file_name)


def delete_photo(path: str) -> None:
    async def _delete_photo(path):
        if path and "media" in path:
            path_exists = os.path.exists(path)
            if path_exists:
                os.remove(path)

    loop = asyncio.get_event_loop()
    loop.create_task(_delete_photo(path))
