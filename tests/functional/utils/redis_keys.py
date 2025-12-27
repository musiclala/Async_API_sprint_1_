from redis.asyncio import Redis


async def keys_count(redis_client: Redis, pattern: str) -> int:
    keys = await redis_client.keys(pattern)
    return len(keys)