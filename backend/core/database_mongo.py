from motor.motor_asyncio import AsyncIOMotorClient

from backend.api_v1.games.models_nosql import UserGamesModel
from .config import get_mongo_uri, get_mongo_db

class MongoController:
    def __init__(self):
        MONGO_URI = get_mongo_uri()
        MONGO_DB = get_mongo_db()
        # TODO: Remove on prod
        MONGO_URI = 'mongodb://root:example@localhost:27017'
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[MONGO_DB]

    async def get_user_games(self, user_id: str):
        return await self.db['user_games'].find_one({'user_id': user_id})

    async def add_user_games(self, user_games: UserGamesModel):
        user_games_dict = user_games.model_dump()
        user_games_dict['games'] = [game.model_dump() for game in user_games.games]
        await self.db['user_games'].insert_one(user_games_dict)
