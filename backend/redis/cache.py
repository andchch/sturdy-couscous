from redis import Redis, asyncio as aioredis

class RedisController():
    redis: Redis
    
    def __init__(self, redis_url: str = 'redis://localhost:6379'):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)
