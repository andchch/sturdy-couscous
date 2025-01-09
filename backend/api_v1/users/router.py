from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile

from backend.core.database_s3 import get_user_avatar, upload_file_to_s3

from .exceptions import user_exists_exception, user_not_exists_exception, self_follow_exception, not_followed_exception
from backend.api_v1.auth.auth import get_password_hash
from backend.api_v1.games.models_nosql import MinecraftModel
from backend.api_v1.users.dao import UserDAO, UserFollowDAO, UserInteractionDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User, UserContacts, UserFollow
from backend.core.database_mongo import MongoController
from backend.api_v1.games.models_nosql import UserGamesModel
from backend.api_v1.users.schemas import GetMeResponse, UpdateMeContactsRequest
from backend.api_v1.users.schemas import (
    CreateUserResponse,
    UpdateMeRequest,
    UpdateCredentialsRequest,
    CreateUserRequest,
)


user_router = APIRouter(prefix='/user', tags=['Users management'])
S3_MEDIA_BUCKET='user.media'


@user_router.post('/register', response_model=CreateUserResponse)
async def register_user(data: CreateUserRequest):
    data = data.model_dump()
    pot_user = await UserDAO.find_all(username=data['username'])
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

'''
TODO:check
@user_router.post('/create_user_interaction')
async def create_user_interaction(u_id1: int, u_id2: int, game: str, u_rating1: str, u_rating2: str):
    try:
        new_user_int = await UserInteractionDAO.create_interaction(
            u_id1, u_id2, game, u_rating1, u_rating2
        )
        return {'status': 'good'}
    except Exception as e:
        return {'status': str(e)}


@user_router.post('/create/ugm')
async def create_ugm(hour: int):
    game = MinecraftModel(hours_played=hour)
    ugm = UserGamesModel(user_id=1, games=[game])
    mongo = MongoController()
    print(ugm.model_dump())
    await mongo.add_user_games(ugm)
'''


@user_router.get('/me')#, response_model=GetMeResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    response = GetMeResponse(
        username=current_user.username,
        email=current_user.email,
        gender=current_user.gender,
        date_of_birth=current_user.dof
    )
    return current_user

@user_router.patch('/{user_id}/change-password')
async def change_password(user_id: int, new_password: str = Form(...)):
    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise user_not_exists_exception
    else:
        await UserDAO.update(user.id, hashed_password=get_password_hash(new_password))
        return {'status': 'password has been changed'}
    
@user_router.patch('/update-me-contacts')
async def update_me_contacts(current_user: Annotated[User, Depends(get_current_user)],
                             data: UpdateMeContactsRequest):
    await UserDAO.update_contacts(current_user.id, data.model_dump())
    
    return {'status': 'good'}
    

@user_router.patch('/update-me')
async def update_me(current_user: Annotated[User, Depends(get_current_user)],
                    gender: str = Form(None), purpose: str = Form(None),
                    self_assessment_lvl: str = Form(None),
                    preferred_communication: str = Form(None),
                    hours_per_week: int = Form(None),
                    new_avatar: UploadFile | None = File(None)):
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

@user_router.get('/get-avatar')
async def get_avatar(user_id: int):
    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise user_not_exists_exception
    else:
        if user.avatar_url is not None:
            file_name = user.avatar_url.split('/')[-1]
            print(file_name)
            avatar_url = get_user_avatar(file_name)
            return {'avatar_url': f'{avatar_url}'}
        else:
            return {'avatar_url': 'no avatar'}

@user_router.post("/{user_id}/follow")
async def follow_user(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id == user_id:
        raise self_follow_exception

    await UserFollowDAO.follow(current_user.id, user_id)
    
    return {"message": "Подписка успешна"}

@user_router.delete("/{user_id}/unfollow")
async def unfollow_user(user_id: int, current_user: User = Depends(get_current_user)):
    is_followed = await UserFollow.check_follow(current_user.id, user_id)
    
    if not is_followed:
        raise not_followed_exception
    else:
        UserFollowDAO.delete(is_followed.id)
        return {"message": "Вы отписались"}

@user_router.get("/{user_id}/followers")
async def get_followers(user_id: int):
    followers = UserFollowDAO.find_all(UserFollow.followed_id == user_id)
    
    return {"followers": [{"id": f.follower.id, "username": f.follower.username} for f in followers]}

@user_router.get("/{user_id}/following")
async def get_following(user_id: int):
    following = UserFollowDAO.find_all(UserFollow.follower_id == user_id)
    
    return {"following": [{"id": f.followed.id, "username": f.followed.username} for f in following]}
