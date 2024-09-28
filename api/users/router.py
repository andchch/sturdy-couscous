from fastapi import APIRouter, HTTPException, status, Depends

from api.auth.auth import get_password_hash
from api.users.dao import UserDAO
from api.users.dependencies import get_current_user
from api.users.models import User, UserCreate

router = APIRouter(prefix='/user', tags=['Users management'])


@router.post('/register')
async def register_user(user_data: UserCreate) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='User already exists'
        )
    # TODO: write it in a good way
    user_dict = user_data.model_dump()
    user_dict['password'] = None
    user_dict['hashed_password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.get('/me')
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data
