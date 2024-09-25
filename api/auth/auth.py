from functools import wraps
from typing import Callable

import jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from api.auth.dao import TokenBlacklistDAO
from api.config import get_auth_data, get_jwt_expiration
from api.auth.exceptions import role_forbidden
from api.users.dao import UserDAO
from api.users.models import User

securing_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str) -> str:
    return securing_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return securing_context.verify(plain_password, hashed_password)


async def verify_token(token: str) -> bool:
    result = await TokenBlacklistDAO.find_one_or_none(token=token)
    print(result)
    if result is None:
        return True
    else:
        return False


def generate_jwt(
    data: dict, expires_delta: timedelta | None = None
) -> str:  # TODO: Implement refresh_token
    payload = data.copy()
    if expires_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(get_jwt_expiration())
    else:
        expire = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expire})
    auth_data = get_auth_data()
    token = jwt.encode(
        payload=payload,
        key=auth_data['secret_key'],
        algorithm=auth_data['algorithm'],
    )
    return token


async def authenticate_user(email: EmailStr, password: str) -> User | None:
    user = await UserDAO.find_one_or_none(email=email)
    if (
        not user
        or verify_password(
            plain_password=password, hashed_password=user.password
        )
        is False
    ):
        return None
    return user


def require_roles(required_roles: list[str]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_data: User = kwargs.get('user_data') or args[0]
            if (
                user_data.id not in required_roles
            ):  # TODO: change to role and add role filed to user
                raise role_forbidden
            return await func(*args, **kwargs)

        return wrapper

    return decorator
