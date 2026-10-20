import json

import redis.asyncio as redis

from .config import settings


async def get_redis_client() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)


async def publish_message(event_type: str, payload: dict) -> None:
    client = await get_redis_client()
    queue_name = "wechat:events"
    await client.lpush(queue_name, json.dumps({"type": event_type, **payload}))
    await client.aclose()
