from __future__ import annotations

import asyncio
import random
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


def expo_backoff(
    *,
    exceptions: tuple[type[Exception], ...],
    start_sleep_time: float = 0.1,
    factor: float = 2.0,
    border_sleep_time: float = 10.0,
    max_retries: int = 7,
    jitter: float = 0.1,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        async def wrapper(*args, **kwargs) -> T:
            sleep_time = start_sleep_time
            last_exc: Exception | None = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc

                    if attempt == max_retries - 1:
                        raise

                    j = 1.0 + random.uniform(-jitter, jitter)
                    await asyncio.sleep(min(sleep_time, border_sleep_time) * j)
                    sleep_time *= factor

            assert last_exc is not None
            raise last_exc

        return wrapper
    return decorator