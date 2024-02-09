from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.config import CACHE_PREFIX, REDIS_URL


redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)


async def init_redis() -> None:
    FastAPICache.init(RedisBackend(redis), prefix=CACHE_PREFIX)
