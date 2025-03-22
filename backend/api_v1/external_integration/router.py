# Получение данных пользователя и их сохранение
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from backend.api_v1.external_integration.dao import SteamProfileDAO
from backend.api_v1.external_integration.dependencies import SteamService, get_steam_service
from backend.api_v1.external_integration.schemas import GetFriendsResponse, GetGamesResponse
from backend.api_v1.external_integration.utilities import fetch_friends, fetch_owned_games, fetch_steam_profile
from backend.api_v1.users.dao import UserDAO
from backend.api_v1.external_integration.exceptions import privacy_error, no_profile_exception
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User
from backend.api_v1.auth.exceptions import auth_failed


ext_integration_router = APIRouter(prefix='/ext', tags=['External integration'])


@ext_integration_router.get('/steam/auth')
async def steam_auth(request: Request, current_user: Annotated[User, Depends(get_current_user)],
                     steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    params = dict(request.query_params)
    if 'openid.claimed_id' not in params:
        raise auth_failed

    steam_id = params['openid.claimed_id'].split('/')[-1]
    user_summary = await fetch_steam_profile(steam_id)
    await UserDAO.update_steam_profile(current_user.id, user_summary)
    await steam_service.update_profile(steam_id, user_summary)

    return RedirectResponse('http://213.171.29.113:5000/docs')
    return {'message': 'Login successful', 'steamid': steam_id}

@ext_integration_router.get('/steam/{user_id}')
async def get_steam_profile(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        raise no_profile_exception
    profile = await steam_service.get_profile(steam_profile.steam_id, user_id)

    return profile

@ext_integration_router.post('/steam/{user_id}/')
async def refresh_steam_data(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        raise no_profile_exception

    steam_id = steam_profile.steam_id

    profile_data = await fetch_steam_profile(steam_id)
    profile_data.update({'user_id': user_id})
    games_data = await fetch_owned_games(steam_id)
    games_data.update({'user_id': user_id})
    friends_data = await fetch_friends(steam_id)
    friends_data.update({'user_id': user_id})

    await steam_service.update_games(steam_id, games_data)
    await steam_service.update_friends(steam_id, friends_data)
    await steam_service.update_profile(steam_id, profile_data)

    return {'status': 'updated'}

@ext_integration_router.get('/steam/{user_id}/games', description='Возвращает данные из локальных бд')#, response_model=GetGamesResponse)
async def get_users_games(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        raise no_profile_exception
    steam_id = steam_profile.steam_id
    
    data = await steam_service.get_games(steam_profile.steam_id)
    
    sorted_games = sorted(
        data['response']['games'],
        key=lambda x: x.get('playtime_forever', 0),
        reverse=True
        )
        
    game_names = [game['name'] for game in sorted_games]
    
    res = {"games": game_names[:50]}
    return game_names[:50]

@ext_integration_router.put('/steam/{user_id}/games', description='Обновляет данные из Steam')
async def fetch_users_games(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        raise no_profile_exception
    new_data = await fetch_owned_games(steam_profile.steam_id)
    new_data.update({'user_id': user_id})
    await steam_service.update_games(steam_profile.steam_id, new_data)
    return await steam_service.get_games(steam_profile.steam_id)
    
@ext_integration_router.get('/steam/{user_id}/friends', response_model=GetFriendsResponse)
async def get_steam_friends(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        raise no_profile_exception
    data = await steam_service.get_friends(steam_profile.steam_id)
    return data

@ext_integration_router.put('/steam/{user_id}/friends')
async def fetch_steam_friends(user_id: int, steam_service: Annotated[SteamService, Depends(get_steam_service)]):
    steam_profile = await SteamProfileDAO.get_by_user_id(user_id)
    if not steam_profile:
        raise no_profile_exception
    new_data = await fetch_friends(steam_profile.steam_id)
    new_data.update({'user_id': user_id})
    if 'error' in new_data.keys() and new_data['error'] == 'privacy':
        raise privacy_error
    return await steam_service.update_friends(steam_profile.steam_id, new_data)
