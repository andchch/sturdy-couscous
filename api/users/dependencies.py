from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from api.auth.exceptions import credentials_exception, revoke_exception
from api.config import get_auth_data
from api.auth.auth import oauth2_scheme, verify_token
from api.users.dao import UserDAO
from api.users.models import User


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    if not await verify_token(token):
        raise revoke_exception
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data['secret_key'], algorithms=[auth_data['algorithm']]
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
