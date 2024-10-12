from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import authenticate_user, generate_jwt, oauth2_scheme

auth_router = APIRouter(prefix='/auth', tags=['Authentication management'])


#  email === password
@auth_router.post('/token')
async def get_token(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(email=user_data.username, password=user_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = generate_jwt(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.post('/logout')
async def revoke_token(token: str = Depends(oauth2_scheme)):
    await TokenBlacklistDAO.add(token=token)
    return {'message': f'Token {token} was successfully revoked'}
