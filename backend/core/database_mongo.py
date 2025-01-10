from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from .config import get_mongo_uri, get_mongo_db

class MongoController:
    def __init__(self):
        MONGO_URI = get_mongo_uri()
        MONGO_DB = get_mongo_db()
        # TODO: Remove on prod
        MONGO_URI = 'mongodb://root:example@localhost:27017'
        MONGO_DB = 'STEAM'
        
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_DB]
        
    async def create_indexes(self):
        await self.db.profiles.create_index('steam_id', unique=True)
        await self.db.profiles.create_index('updated_at', expireAfterSeconds=604800)
        await self.db.games.create_index('steam_id')
        await self.db.achievements.create_index('steam_id')
        await self.db.friends.create_index('steam_id')

    async def save_data(self, collection: str, steam_id: str, data: dict):
        data['steam_id'] = steam_id
        data['updated_at'] = datetime.now()
        await self.db[collection].update_one({'steam_id': steam_id}, {'$set': data}, upsert=True)

    async def get_data(self, collection: str, steam_id: str):
        return await self.db[collection].find_one({'steam_id': steam_id})

"""
async def get_user_games(self, user_id: str):
        return await self.db['user_games'].find_one({'user_id': user_id})

    async def add_user_games(self, user_games: UserGamesModel):
        user_games_dict = user_games.model_dump()
        user_games_dict['games'] = [game.model_dump() for game in user_games.games]
        await self.db['user_games'].insert_one(user_games_dict)

    async def save_attachment(data: bytes, post_id: int):
        result = await attachments_collection.insert_one({"post_id": post_id, "data": data})
        return str(result.inserted_id)

    async def get_attachments(post_id: int):
        attachments = await attachments_collection.find({"post_id": post_id}).to_list(length=100)
        return attachments
"""
    