from __future__ import annotations

import abc
from typing import Any


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str) -> Any | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def make_key(self, prefix: str, *parts: Any) -> str:
        raise NotImplementedError