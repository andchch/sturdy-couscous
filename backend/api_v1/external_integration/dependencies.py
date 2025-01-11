import json
from backend.api_v1.external_integration.dao import SteamProfileDAO
from backend.api_v1.external_integration.utilities import DateTimeEncoder
from backend.api_v1.external_integration.exceptions import privacy_error
from backend.core.database_mongo import MongoController
from backend.redis.cache import RedisController


class SteamService:
    def __init__(self, mongo_controller: MongoController, redis_controller: RedisController):
        self.mongo = mongo_controller
        self.redis = redis_controller.redis

    async def get_profile(self, steam_id: str, user_id: int):
        """Get steam profile from service database"""
        cache_key = f'steam:profile:{steam_id}'
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        
        profile = await self.mongo.get_data('profile', steam_id)
        if profile:
            await self.redis.set(cache_key, json.dumps(profile, cls=DateTimeEncoder), ex=86400)
        return profile
        
        sql_profile = SteamProfileDAO.get_by_user_id(user_id)
        if sql_profile:
            profile_data = {
                'steam_id': sql_profile.steam_id,
                'steam_name': sql_profile.steam_name,
                'steam_avatar': sql_profile.steam_avatar,
                'profile_url': sql_profile.profile_url
            }
            await self.redis.set(cache_key, json.dumps(profile_data, cls=DateTimeEncoder), ex=86400)
            return profile_data
        
    async def update_profile(self, steam_id: int, data: dict):
        await self.mongo.save_data('profile', steam_id, data)
        cache_key = f'steam:profile:{steam_id}'
        await self.redis.set(cache_key, json.dumps(data, cls=DateTimeEncoder), ex=86400)

    async def get_games(self, steam_id: str):
        cache_key = f'steam:games:{steam_id}'
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            # del cached_data['_id']
            return json.loads(cached_data)
        
        games = await self.mongo.get_data('games', steam_id)
        if games:
            del games['_id']
            await self.redis.set(cache_key, json.dumps(games, cls=DateTimeEncoder), ex=86400)
        return games

    async def update_games(self, steam_id: str, data: dict):
        await self.mongo.save_data('games', steam_id, data)
        cache_key = f'steam:games:{steam_id}'
        await self.redis.set(cache_key, json.dumps(data, cls=DateTimeEncoder), ex=86400)

    async def get_achievements(self, steam_id: str):
        cache_key = f'steam:achievements:{steam_id}'
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        
        achievements = await self.mongo.get_data('achievements', steam_id)
        if achievements:
            await self.redis.set(cache_key, json.dumps(achievements, cls=DateTimeEncoder), ex=86400)
        return achievements

    async def update_achievements(self, steam_id: str, data: dict):
        await self.mongo.save_data('achievements', steam_id, data)
        cache_key = f'steam:achievements:{steam_id}'
        await self.redis.set(cache_key, json.dumps(data, cls=DateTimeEncoder), ex=86400)

    async def get_friends(self, steam_id: str):
        cache_key = f'steam:friends:{steam_id}'
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        
        friends = await self.mongo.get_data('friends', steam_id)
        if friends:
            if friends['error'] == 'privacy':
                raise privacy_error
            await self.redis.set(cache_key, json.dumps(friends, cls=DateTimeEncoder), ex=86400)
        return friends

    async def update_friends(self, steam_id: str, data: dict):
        await self.mongo.save_data('friends', steam_id, data)
        cache_key = f'steam:friends:{steam_id}'
        await self.redis.set(cache_key, json.dumps(data, cls=DateTimeEncoder), ex=86400)
        
def get_steam_service() -> SteamService:
    mongo = MongoController()
    redis = RedisController()
    service = SteamService(mongo, redis)
    return service
