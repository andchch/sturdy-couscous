from redis import asyncio as aioredis


class RedisController():
    def __init__(self, redis_url: str = 'redis://localhost'):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)
