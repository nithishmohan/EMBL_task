
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend


def redis_cache():
    return caches.get(CACHE_KEY)


async def connect(host, port, index) -> None:
    rc = RedisCacheBackend('redis://{0}:{1}/{2}'.format(host, port, index))
    caches.set(CACHE_KEY, rc)


async def close() -> None:
    await close_caches()



