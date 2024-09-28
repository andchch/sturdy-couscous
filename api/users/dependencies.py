from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from api.auth.exceptions import credentials_exception, revoke_exception
from api.config import get_jwt_settings
from api.auth.auth import oauth2_scheme, verify_token
from api.users.dao import UserDAO
from api.users.models import User


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    if not await verify_token(token):
        raise revoke_exception
    try:
        jwt_settings = get_jwt_settings()
        payload = jwt.decode(
            token,
            jwt_settings['secret_key'],
            algorithms=[jwt_settings['algorithm']],
        )
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await UserDAO.find_one_or_none(email=email)
    if user is None:
        raise credentials_exception

    return user
