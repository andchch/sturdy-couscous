from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile

from backend.core.database_s3 import upload_file_to_s3

from .exceptions import user_exists_exception
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
S3_MEDIA_BUCKET='user.media'


@user_router.post('/register', response_model=CreateUserResponse)
async def create_user(data: CreateUserRequest):
    data = data.model_dump()
    pot_user = await UserDAO.find_all(username=data['username'])
    print(pot_user)
    if pot_user != []:
        raise user_exists_exception
    
    new_user = await UserDAO.create(
        username=data['username'],
        email=data['email'],
        hashed_password=get_password_hash(data['password']),
    )
    response = CreateUserResponse(status='good',
                                  description='')
    return response

#TODO:check
# @user_router.post('/create_user_interaction')
# async def create_user_interaction(u_id1: int, u_id2: int, game: str, u_rating1: str, u_rating2: str):
#     try:
#         new_user_int = await UserInteractionDAO.create_interaction(
#             u_id1, u_id2, game, u_rating1, u_rating2
#         )
#         return {'status': 'good'}
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
    avatar_url_str = str(current_user.avatar_url) if current_user.avatar_url is not None else None
    response = GetMeResponse(
        username=current_user.username,
        email=current_user.email,
        gender=current_user.gender,
        date_of_birth=current_user.dof,
        avatar_url=avatar_url_str,
        steam_id=current_user.steam_id,
        purpose=current_user.purpose,
        self_assessment_lvl=current_user.self_assessment_lvl,
        preferred_communication=current_user.preferred_communication,
        hours_per_week=current_user.hours_per_week
    )
    return response


@user_router.patch('/updateme')
async def update_me(current_user: Annotated[User, Depends(get_current_user)],
                    gender: str = Form(None), purpose: str = Form(None),
                    self_assessment_lvl: str = Form(None),
                    preferred_communication: str = Form(None),
                    hours_per_week: int = Form(None),
                    new_avatar: UploadFile | None = File(None)):
                    #data: UpdateMeRequest):
    # data = data.model_dump()
    if new_avatar is not None:
        file_url = upload_file_to_s3(new_avatar, S3_MEDIA_BUCKET)
        await UserDAO.update(current_user.id, gender=gender, purpose=purpose,
                            self_assessment_lvl=self_assessment_lvl,
                            preferred_communication=preferred_communication,
                            hours_per_week=hours_per_week,
                            avatar_url=file_url)
    else:
        await UserDAO.update(current_user.id, gender=gender, purpose=purpose,
                            self_assessment_lvl=self_assessment_lvl,
                            preferred_communication=preferred_communication,
                            hours_per_week=hours_per_week)
    return {'status': 'good'}


# @user_router.patch('/updatecreds')
# async def update_credentials(current_user: Annotated[User, Depends(get_current_user)], data: UpdateCredentialsRequest):
#     user = await UserDAO.get_by_email(current_user.email)
#     data = data.model_dump()
#     await UserDAO.update(user.id, username=data['username'])
#     return {'status': 'good'}
