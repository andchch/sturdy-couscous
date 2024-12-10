from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy import select

from backend.api_v1.games.models_nosql import GameModel, UserGamesModel
from backend.api_v1.games.models_sql import Game
from backend.core.dao import BaseDAO
from backend.core.database_sql import async_session

class GameDAO(BaseDAO[Game]):
    model = Game
    
    @classmethod
    async def get_by_app_steam_id(cls, appid: str, steamid: str) -> Optional[Game]:
        async with async_session() as session:
            query = select(cls.model).where(cls.model.appid == appid, cls.model.steamid == steamid)
            result = await session.execute(query)
            return result.scalar_one_or_none()

class GameDAO_Mongo:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.games_collection = self.db.user_games

    async def get_user_games(self, user_id: str) -> Optional[UserGamesModel]:
        result = await self.games_collection.find_one({'user_id': user_id})
        return UserGamesModel(**result) if result else None

    async def add_user_games(self, user_games: UserGamesModel) -> bool:
        result = await self.games_collection.insert_one(user_games.dict())
        return result.acknowledged

    async def update_user_games(self, user_id: str, games: List[GameModel]) -> bool:
        result = await self.games_collection.update_one(
            {'user_id': user_id},
            {'$set': {'games': [game.dict() for game in games]}}
        )
        return result.modified_count > 0

    async def delete_user_games(self, user_id: str) -> bool:
        result = await self.games_collection.delete_one({'user_id': user_id})
        return result.deleted_count > 0

    async def add_game_to_user(self, user_id: str, game: GameModel) -> bool:
        result = await self.games_collection.update_one(
            {'user_id': user_id},
            {'$push': {'games': game.dict()}}
        )
        return result.modified_count > 0 