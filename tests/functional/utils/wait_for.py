import asyncio

import aiohttp
import redis.asyncio as redis


async def wait_for_es(es_url: str, timeout_s: int = 60) -> None:
    async with aiohttp.ClientSession() as session:
        for _ in range(timeout_s):
            try:
                async with session.get(es_url, timeout=aiohttp.ClientTimeout(total=2)) as resp:
                    if resp.status < 500:
                        return
            except Exception:
                pass
            await asyncio.sleep(1)
    raise RuntimeError(f"Elasticsearch not ready: {es_url}")


async def wait_for_redis(host: str, port: int, timeout_s: int = 60) -> None:
    r = redis.Redis(host=host, port=port)
    try:
        for _ in range(timeout_s):
            try:
                pong = await r.ping()
                if pong:
                    return
            except Exception:
                pass
            await asyncio.sleep(1)
    finally:
        await r.aclose()
    raise RuntimeError(f"Redis not ready: {host}:{port}")


async def wait_for_api(api_url: str, timeout_s: int = 60) -> None:
    async with aiohttp.ClientSession() as session:
        for _ in range(timeout_s):
            try:
                async with session.get(f"{api_url}/openapi.json", timeout=aiohttp.ClientTimeout(total=2)) as resp:
                    if resp.status < 500:
                        return
            except Exception:
                pass
            await asyncio.sleep(1)
    raise RuntimeError(f"API not ready: {api_url}")


async def wait_all(
    es_url: str,
    redis_host: str,
    redis_port: int,
    api_url: str,
) -> None:
    await wait_for_es(es_url)
    await wait_for_redis(redis_host, redis_port)
    await wait_for_api(api_url)