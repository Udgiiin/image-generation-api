from aioredis import Redis, from_url
from app.core.config import settings

async def create_redis_pool():
    pool = await from_url(
        f"redis://{settings.REDIS}", decode_responses=True
    )
    return await pool


