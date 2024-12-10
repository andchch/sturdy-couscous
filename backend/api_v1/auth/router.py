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
        'openid.return_to': 'http://87.242.103.34:8000/auth/auth_steam',
        'openid.realm': 'http://87.242.103.34:8000/',
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





# @auth_router.post('/logout')
# async def revoke_token(token: str = Depends(oauth2_scheme)):
#     await TokenBlacklistDAO.add(token=token)
#     return {'message': f'Token {token} was successfully revoked'}
