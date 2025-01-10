# Получение данных пользователя и их сохранение
from typing import Annotated
from fastapi import APIRouter, Depends, Request

from backend.api_v1.external_integration.dao import SteamProfileDAO
from backend.api_v1.external_integration.dependencies import SteamService, get_steam_service
from backend.api_v1.external_integration.utilities import fetch_achievements, fetch_friends, fetch_owned_games, fetch_steam_profile
from backend.api_v1.users.dao import UserDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User
from backend.api_v1.auth.exceptions import auth_failed


ext_integration_router = APIRouter(prefix='/ext', tags=['External integration'])


@ext_integration_router.post('/steam/auth')
async def steam_auth(request: Request, current_user: Annotated[User, Depends(get_current_user)],
                     steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    params = dict(request.query_params)
    if 'openid.claimed_id' not in params:
        raise auth_failed

    steam_id = params['openid.claimed_id'].split('/')[-1]
    user_summary = await fetch_steam_profile(steam_id)
        
    await UserDAO.update_steam_profile(current_user.id, **user_summary)
    await steam_service.update_profile(steam_id, user_summary)

    return {'message': 'Login successful', 'steamid': steam_id}

@ext_integration_router.get('/steam/{user_id}')
async def get_steam_profile(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        return {'error': 'Steam profile not found'}
    profile = await steam_service.get_profile(steam_profile.steam_id, user_id)

    return profile

@ext_integration_router.post('/steam/{user_id}/')
async def refresh_steam_data(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        return {'error': 'Steam profile not found'}

    steam_id = steam_profile.steam_id

    profile_data = await fetch_steam_profile(steam_id)
    games_data = await fetch_owned_games(steam_id)
    friends_data = await fetch_friends(steam_id)

    steam_service.update_games(steam_id, games_data)
    steam_service.update_friends(steam_id, friends_data)
    steam_service.update_profile(steam_id, profile_data)

    return {'status': 'updated'}

@ext_integration_router.get('/steam/{user_id}/games', description='Возвращает данные из локальных бд')
async def get_users_games(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    return await steam_service.get_games(steam_profile.steam_id)

@ext_integration_router.put('/steam/{user_id}/games', description='Обновляет данные из Steam')
async def get_users_games(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    new_data = fetch_owned_games(steam_profile.steam_id)
    await steam_service.update_games(steam_profile.steam_id, new_data)
    return await steam_service.get_games(steam_profile.steam_id)

@ext_integration_router.get('/steam/{user_id}/achievements')
async def get_steam_achievements(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    return await steam_service.get_achievements(steam_profile.steam_id)

#TODO: for many games
@ext_integration_router.put('/steam/{user_id}/achievements')
async def get_steam_achievements(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    new_data = fetch_achievements(steam_profile.steam_id)
    
@ext_integration_router.get('/steam/{user_id}/friends')
async def get_steam_friends(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    return await steam_service.get_friends(steam_profile.steam_id)

@ext_integration_router.put('/steam/{user_id}/friends')
async def get_steam_friends(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    new_data = fetch_friends(steam_profile.steam_id)
    return await steam_service.update_friends(steam_profile.steam_id, new_data)






"""
@ext_integration_router.get('/{user_id}/steam')
async def get_users_integrations(user_id: int):
    # data = await UserIntegroTableDAO.get_integrations(user_id)
    return {'user_id': data.user_id,
            'steam_id': data.steam_id}


@ext_integration_router.get('/fetch-data')
async def fetch_data(steamid: str):
    owned_games = fetch_owned_games(get_steam_api_key(), steamid)

    # Сохранение игр
    for game in owned_games:
        db_game = GameDAO.get_by_app_steam_id(game['appid'], steamid)
        if not db_game:
            db_game = Game(
                steamid=steamid,
                appid=game['appid'],
                name=game['name'],
                playtime_hours=game['playtime_forever'] / 60,
            )
            GameDAO.create(db_game)

    # Сохранение достижений
    for game in owned_games:
        appid = game['appid']
        game_achievements = fetch_achievements(get_steam_api_key(), steamid, appid)
        for achievement in game_achievements:
            db_achievement = AchievementDAO.get_by_app_steam_id(
                appid, steamid, achievement['name']
            )

            if not db_achievement:
                db_achievement = Achievement(
                    steamid=steamid,
                    appid=appid,
                    achievement=achievement['name'],
                    unlocked=achievement['unlocked'],
                )
                AchievementDAO.create(db_achievement)

    return {'message': 'Data fetched and saved'}
"""