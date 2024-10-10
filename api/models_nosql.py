from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional


class FavoriteGame(BaseModel):
    game_name: str
    rank: Optional[str]
    position: Optional[str]
    achievements: Optional[List[str]]
    rating: Optional[int]

class UserGames(BaseModel):
    user_id: str
    favorite_games: List[FavoriteGame]

class GameInteraction(BaseModel):
    user_id: str
    partner_id: str
    game_name: str
    interaction_date: str
    rating: int
    success: bool


class MongoDB:
    def __init__(self, mongo_uri: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client['game_recommendation']

    async def get_user_games(self, user_id: str):
        return await self.db['user_games'].find_one({'user_id': user_id})

    async def add_user_games(self, user_games: UserGames):
        await self.db['user_games'].insert_one(user_games.dict())

    async def get_game_interactions(self, user_id: str):
        return await self.db['game_interactions'].find({'user_id': user_id}).to_list(length=100)
    
    async def add_game_interaction(self, interaction: GameInteraction):
        await self.db['game_interactions'].insert_one(interaction.dict())
