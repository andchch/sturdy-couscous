from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.auth.auth import get_password_hash
from backend.api_v1.games.models_nosql import MinecraftModel
from backend.api_v1.users.dao import UserDAO, UserInteractionDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User
from backend.core.database_mongo import MongoController
from backend.api_v1.games.models_nosql import UserGamesModel
from backend.api_v1.users.schemas import GetMeResponse
from backend.api_v1.users.schemas import (
    CreateUserResponse,
    UpdateMeRequest,
    UpdateCredentialsRequest,
    CreateUserRequest,
)


user_router = APIRouter(prefix='/user', tags=['Users management'])


@user_router.post('/register', response_model=CreateUserResponse)
async def create_user(data: CreateUserRequest):
    data = data.model_dump()
    try:
        new_user = await UserDAO.create(
            username=data['username'],
            email=data['email'],
            hashed_password=get_password_hash(data['password']),
        )
        response = CreateUserResponse()
        return response
    except Exception as e:
        return {'status': str(e)}


# @user_router.post('/create_user_interaction')
# async def create_user_interaction(id1: int, id2: int, game: str, u1r: str, u2r: str):
#     try:
#         new_user_int = await UserInteractionDAO.create_interaction(
#             id1, id2, game, u1r, u2r
#         )
#         return new_user_int
#     except Exception as e:
#         return {'status': str(e)}


# @user_router.post('/create/ugm')
# async def create_ugm(hour: int):
#     game = MinecraftModel(hours_played=hour)
#     ugm = UserGamesModel(user_id=1, games=[game])
#     mongo = MongoController()
#     print(ugm.model_dump())
#     await mongo.add_user_games(ugm)


@user_router.get('/me', response_model=GetMeResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    response = GetMeResponse(
        username=current_user.username,
        email=current_user.email,
        gender=current_user.gender,
        date_of_birth=current_user.dof,
    )
    return response


@user_router.patch('/updateme')
async def update_me(
    current_user: Annotated[User, Depends(get_current_user)], data: UpdateMeRequest
):
    user = await UserDAO.get_by_email(current_user.email)
    print(f'user_id: {user.id}')
    print(f'model_dump: {data.model_dump()}')
    data = data.model_dump()
    await UserDAO.update(user.id, **data)
    return {'status': 'good'}


@user_router.patch('/updatecreds')
async def update_credentials(
    current_user: Annotated[User, Depends(get_current_user)],
    data: UpdateCredentialsRequest,
):
    user = await UserDAO.get_by_email(current_user.email)
    data = data.model_dump()
    await UserDAO.update(user.id, username=data['username'])
    return {'status': 'good'}
