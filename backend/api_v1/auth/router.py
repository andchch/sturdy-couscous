from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from backend.api_v1.auth.schemas import GetTokenResponse

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
@auth_router.get('/steam/login')
async def login_steam():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': 'http://87.242.103.34:8000/ext/steam/auth',
        'openid.realm': 'http://87.242.103.34:8000/',
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }
    login_url = f'{"https://steamcommunity.com/openid/login"}?{urlencode(params)}'
    return RedirectResponse(login_url)
