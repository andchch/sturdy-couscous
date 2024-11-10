from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .exceptions import invalid_login_pass
from .auth import authenticate_user, generate_jwt


auth_router = APIRouter(prefix='/auth', tags=['Authentication management'])


@auth_router.post('/token')
async def get_token(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(email=user_data.username, password=user_data.password)
    if user is None:
        raise invalid_login_pass

    access_token = generate_jwt(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


# @auth_router.post('/logout')
# async def revoke_token(token: str = Depends(oauth2_scheme)):
#     await TokenBlacklistDAO.add(token=token)
#     return {'message': f'Token {token} was successfully revoked'}
