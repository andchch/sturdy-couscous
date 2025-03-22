from typing import Annotated

import jwt
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from backend.api_v1.users.dao import UserDAO
from backend.api_v1.users.models_sql import User
from backend.core.config import get_auth_data
from backend.api_v1.auth.auth import oauth2_scheme
from backend.api_v1.auth.exceptions import credentials_exception
from backend.core.database_sql import async_session


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data['secret_key'], algorithms=[auth_data['algorithm']]
        )
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await UserDAO.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user

async def get_db():
    async with async_session() as session:
        yield session
        