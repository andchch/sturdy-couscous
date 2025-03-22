import json
from typing import Annotated
import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Query

from backend.api_v1.games.schemas import GetSteamGamesResponse
from backend.redis.cache import RedisController, get_redis_controller


STEAM_API_URL = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
game_router = APIRouter(prefix='/game', tags=['Games management'])


@game_router.get('/api/steam/games', response_model=GetSteamGamesResponse)
async def search_steam_games(
    rediska: Annotated[RedisController, Depends(get_redis_controller)],
    query: str = Query(..., min_length=3, description='Поисковый запрос')
    ):
    # Проверка кеша
    cached = await rediska.redis.get(query)
    if cached:
        return json.loads(cached)
    
    # Запрос к Steam API
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(STEAM_API_URL) as response:
                data = await response.json()
                games = data['applist']['apps']
        except Exception as e:
            raise HTTPException(status_code=503, detail='Steam API недоступен')

    # Фильтрация и форматирование
    filtered = [
        {
            'app_id': game['appid'], 
            'name': game['name']
            }
        for game in games
        if query.lower() in game['name'].lower()
    ][:10]

    # Сохранение в кеш (24 часа)
    await rediska.redis.setex(query, 86400, json.dumps(filtered))
    
    return {'results': filtered}
