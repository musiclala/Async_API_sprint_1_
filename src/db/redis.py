import redis.asyncio as redis

from src.core.config import settings

rds: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    return rds


async def init_redis() -> None:
    global rds
    rds = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=False,
    )


async def close_redis() -> None:
    global rds
    if rds is not None:
        await rds.close()
        rds = None