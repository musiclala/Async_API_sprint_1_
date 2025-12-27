from __future__ import annotations

import orjson
from typing import Any

from redis.asyncio import Redis

from src.core.backoff import expo_backoff
from src.core.config import settings


class RedisCacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = settings.elastic_ttl

    @staticmethod
    def make_key(prefix: str, *parts: Any) -> str:
        safe = ":".join(str(p).replace(":", "_") for p in parts)
        return f"{prefix}:{safe}"

    @expo_backoff(exceptions=(Exception,), start_sleep_time=0.05, max_retries=5)
    async def get(self, key: str) -> Any | None:
        data = await self.redis.get(key)
        if data is None:
            return None
        return orjson.loads(data)

    @expo_backoff(exceptions=(Exception,), start_sleep_time=0.05, max_retries=5)
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        payload = orjson.dumps(value)
        await self.redis.setex(key, ttl or self.ttl, payload)

    @expo_backoff(exceptions=(Exception,), start_sleep_time=0.05, max_retries=5)
    async def flush(self) -> None:
        await self.redis.flushdb()