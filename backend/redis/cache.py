from backend.core.config import get_redis_db

from redis import Redis
from redis import asyncio as aioredis


class RedisController():
    redis: Redis
    
    def __init__(self):
        self.redis = aioredis.from_url(get_redis_db(), decode_responses=True)

def get_redis_controller() -> RedisController:
    redis = RedisController()
    return redis
