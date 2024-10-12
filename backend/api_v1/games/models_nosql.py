from typing import Union
from pydantic import BaseModel


class CounterStrike2Model(BaseModel):
    game_name: str = 'Counter Strike 2'
    hours_played: int
    rank: str
    level: int

class Dota2Model(BaseModel):
    game_name: str = 'DOTA 2'
    hours_played: int
    rank: str
    preferred_position: str
    main_hero: str

class MinecraftModel(BaseModel):
    game_name: str = 'Minecraft'
    hours_played: int


class GameModel(BaseModel):
    __root__: Union[CounterStrike2Model, Dota2Model, MinecraftModel]
    