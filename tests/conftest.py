import os
from contextlib import asynccontextmanager
from subprocess import run as sp_run
from time import sleep
from typing import AsyncGenerator

import pytest
from fastapi_users.password import PasswordHelper
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool, insert
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.auth.models import User
from src.database.database import Base, get_async_session
from src.database.redis import init_redis
from src.main import app

DATABASE_URL_TEST = f"postgresql+asyncpg://test_u:test_p@localhost:5777/test_db"
DB_CONTAINER = "postgres_tests_cats"
DB_VOLUME = f"{os.path.basename(os.getcwd())}_postgres_tests_data"


async def create_database():
    sp_run(["docker", "compose", "up", "postgres_tests", "redis", "-d"])
    while True:
        sleep(1)
        res = sp_run(
            ["docker", "inspect", "-f", "{{json .State.Health.Status}}", DB_CONTAINER],
            capture_output=True,
            text=True,
        )
        if "healthy" in res.stdout:
            break

    global engine_test
    engine_test = create_async_engine(
        DATABASE_URL_TEST,
        poolclass=NullPool,  # TODO
    )
    global async_session_maker
    async_session_maker = sessionmaker(
        engine_test, class_=AsyncSession, expire_on_commit=False
    )

    Base.metadata.bind = engine_test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    print("DROP")
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    sp_run(["docker", "stop", DB_CONTAINER])
    sp_run(["docker", "rm", "-f", DB_CONTAINER])
    sp_run(["docker", "volume", "rm", DB_VOLUME])


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


get_session_context = asynccontextmanager(override_get_async_session)


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    await create_database()
    yield
    await drop_database()


@pytest.fixture(scope="session")
async def ac():
    app.dependency_overrides[get_async_session] = override_get_async_session
    async with AsyncClient(ASGITransport(app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def admin_data(ac: AsyncClient):
    password = "T3st12345$"
    admin_data = {
        "email": "test@test.com",
        "hashed_password": PasswordHelper().hash(password),
        "is_superuser": True,
        "is_active": True,
        "is_verified": True,
    }
    async with async_session_maker() as session:
        stmt = insert(User).values(**admin_data)
        await session.execute(stmt)
        await session.commit()

    admin_data["password"] = password
    return admin_data


@pytest.fixture(autouse=True, scope="session")
async def init_cache():
    await init_redis()
