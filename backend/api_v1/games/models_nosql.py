from pydantic import BaseModel


class GameModel(BaseModel):
    game_name: str
    hours_played: int

class CounterStrike2Model(GameModel):
    game_name: str = 'Counter Strike 2'
    rank: str
    level: int

class Dota2Model(GameModel):
    game_name: str = 'DOTA 2'
    rank: str
    preferred_position: str
    main_hero: str

class MinecraftModel(GameModel):
    game_name: str = 'Minecraft'


class UserGamesModel(BaseModel):
    user_id: int
    games: list[CounterStrike2Model | Dota2Model | MinecraftModel]