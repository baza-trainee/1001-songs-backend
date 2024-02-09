from fastapi import FastAPI
from sqlalchemy import func, select

from src.database.database import get_async_session
from src.config import settings
from src.database.redis import init_redis, redis
from src.auth.utils import create_user
from src.auth.models import User
from src.footer.utils import create_footer
from src.our_team.utils import create_fake_team
from src.payment.utils import create_payment
from src.database.fake_data import FAKE_FOOTER, PAYMENT_DATA, FAKE_TEAM


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

    await lock.release()
    yield
