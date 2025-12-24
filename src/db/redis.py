import redis.asyncio as redis

from src.core.config import REDIS_HOST, REDIS_PORT

rds: redis.Redis | None = None


async def get_redis() -> redis.Redis:
    return rds


async def init_redis() -> None:
    global rds
    rds = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=False,
    )


async def close_redis() -> None:
    global rds
    if rds is not None:
        await rds.close()
        rds = None