from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request, requests
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.api_v1.auth.schemas import GetTokenResponse
from backend.api_v1.games.dao import GameDAO
from backend.api_v1.games.models_sql import Achievement, Game
from backend.api_v1.users.dao import AchievementDAO, UserDAO
from backend.api_v1.users.models_sql import User
from backend.core.config import get_steam_api_key

from .exceptions import invalid_login_pass
from .auth import authenticate_user, generate_jwt


auth_router = APIRouter(prefix='/auth', tags=['Authentication management'])


@auth_router.post('/token', response_model=GetTokenResponse)
async def get_token(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(email=user_data.username, password=user_data.password)
    if user is None:
        raise invalid_login_pass

    access_token = generate_jwt(data={'sub': user.email})

    return {'token': access_token, 'token_type': 'bearer'}


# Авторизация через OpenID
@auth_router.get('/login_steam')
async def login_steam():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': 'http://127.0.0.1:8000/auth/auth_steam',
        'openid.realm': 'http://127.0.0.1:8000/',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }
    login_url = f'{"https://steamcommunity.com/openid/login"}?{urlencode(params)}'
    return RedirectResponse(login_url)


@auth_router.get('/auth_steam')
async def auth(request: Request):
    params = dict(request.query_params)
    if 'openid.claimed_id' not in params:
        raise HTTPException(status_code=400, detail='Authorization failed')

    steamid = params['openid.claimed_id'].split('/')[-1]
    user_data = fetch_user_summary(get_steam_api_key(), steamid)

    # Сохранение или обновление данных пользователя
    user = UserDAO.get_by_steamid(steamid)
    if not user:
        # TODO: Raise a error!
        pass
    else:
        UserDAO.update(
            user.id,
            personaname=user_data['personaname'],
            profileurl=user_data['profileurl'],
            avatar=user_data['avatar'],
        )

    return {'message': 'Login successful', 'steamid': steamid}


# Получение данных пользователя и их сохранение
@auth_router.get('/fetch-data')
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


# Функции работы с API Steam
def fetch_user_summary(api_key, steamid):
    url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'
    params = {'key': api_key, 'steamids': steamid}
    response = requests.get(url, params=params).json()
    return response['response']['players'][0]


def fetch_owned_games(api_key, steamid):
    url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
    params = {'key': api_key, 'steamid': steamid, 'include_appinfo': True}
    response = requests.get(url, params=params).json()
    return response['response']['games']


def fetch_achievements(api_key, steamid, appid):
    url = 'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/'
    params = {'key': api_key, 'steamid': steamid, 'appid': appid}
    response = requests.get(url, params=params).json()
    return response['playerstats']['achievements']


# @auth_router.post('/logout')
# async def revoke_token(token: str = Depends(oauth2_scheme)):
#     await TokenBlacklistDAO.add(token=token)
#     return {'message': f'Token {token} was successfully revoked'}
