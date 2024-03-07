from typing import Union

from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.config import CACHE_PREFIX, REDIS_URL


redis = aioredis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
cache_key = (
    lambda func, id, paginate: f"{CACHE_PREFIX}:{func}{f':{id}' if id else ''}{f':{paginate}' if paginate else ''}"
)


async def init_redis() -> None:
    FastAPICache.init(RedisBackend(redis), prefix=CACHE_PREFIX)
    await FastAPILimiter.init(redis)


async def invalidate_cache(func: str, id: int = None, paginate: str = None):
    key = cache_key(func, id, paginate)
    await redis.delete(key)


async def invalidate_cache_partial(func: str):
    keys = await redis.keys(f"{CACHE_PREFIX}:{func}*")
    for key in keys:
        await redis.delete(key)


def my_key_builder(func, *args, **kwargs):
    id = kwargs.get("kwargs").get("id")
    paginate = str(kwargs.get("request").query_params)
    return cache_key(func.__name__, id, paginate)
