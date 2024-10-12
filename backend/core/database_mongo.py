from motor.motor_asyncio import AsyncIOMotorClient

from core.config import get_mongo_uri

class MongoController:
    def __init__(self):
        MONGO_URI = get_mongo_uri()
        # TODO: Remove on prod
        MONGO_URI = 'mongodb://localhost:27017'
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client['game_recommendation']

    async def get_user_games(self, user_id: str):
        return await self.db['user_games'].find_one({'user_id': user_id})

    async def add_user_games(self, user_games: UserGames):
        await self.db['user_games'].insert_one(user_games.dict())

    async def get_game_interactions(self, user_id: str):
        return await self.db['game_interactions'].find({'user_id': user_id}).to_list(length=100)
    
    async def add_game_interaction(self, interaction: GameInteraction):
        await self.db['game_interactions'].insert_one(interaction.dict())
        