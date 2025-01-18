from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from backend.api_v1.auth.auth import get_password_hash
from backend.api_v1.communities.dao import CommunityDAO, CommunityMembershipDAO
from backend.api_v1.users.dao import UserDAO, UserFollowDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User
from backend.api_v1.users.schemas import (
    ContactsSchema,
    CreateUserRequest,
    CreateUserResponse,
    GetAllUsersResponse,
    GetAvatarResponse,
    GetFollowersResponse,
    GetFollowingsResponse,
    GetMeResponse,
    GetUserResponse,
    OnlyStatusResponse,
    UpdateCreditsRequest,
    UpdateCurrentUserRequest,
    UpdateMeContactsRequest,
    UserInfoScheme,
)
from backend.core.database_s3 import get_cached_avatar_url, upload_file_to_s3
from backend.redis.cache import RedisController, get_redis_controller

from .exceptions import (
    already_followed_exception,
    busy_username_exception,
    not_followed_exception,
    self_follow_exception,
    user_exists_exception,
    user_not_exists_exception,
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
    response = CreateUserResponse(status=f'User {new_user.username} created successfully',
                                  description='')
    return response

"""
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
"""


@user_router.get('/me', response_model=GetMeResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.contacts:
        if current_user.info:
            response = GetMeResponse(
                id=current_user.id,
                email=current_user.email,
                username=current_user.username,
                registration_time=current_user.created_at,
                gender=current_user.gender,
                dof=current_user.dof,
                avatar_url=current_user.avatar_url,
                contacts=ContactsSchema(vk=current_user.contacts.vk,
                                        telegram=current_user.contacts.telegram,
                                        steam=current_user.contacts.steam,
                                        discord=current_user.contacts.discord),
                info=UserInfoScheme(purpose=current_user.info.purpose,
                                    self_assessment_lvl=current_user.info.self_assessment_lvl,
                                    preferred_communication=current_user.info.preferred_communication,
                                    hours_per_week=current_user.info.hours_per_week)
                )
        else:
            response = GetMeResponse(
                id=current_user.id,
                email=current_user.email,
                username=current_user.username,
                registration_time=current_user.created_at,
                gender=current_user.gender,
                dof=current_user.dof,
                avatar_url=current_user.avatar_url,
                contacts=ContactsSchema(vk=current_user.contacts.vk,
                                        telegram=current_user.contacts.telegram,
                                        steam=current_user.contacts.steam,
                                        discord=current_user.contacts.discord),
                info=None
                )
    else:
        if current_user.info:
            response = GetMeResponse(
                id=current_user.id,
                email=current_user.email,
                username=current_user.username,
                registration_time=current_user.created_at,
                gender=current_user.gender,
                dof=current_user.dof,
                avatar_url=current_user.avatar_url,
                contacts=None,
                info=UserInfoScheme(purpose=current_user.info.purpose,
                                    self_assessment_lvl=current_user.info.self_assessment_lvl,
                                    preferred_communication=current_user.info.preferred_communication,
                                    hours_per_week=current_user.info.hours_per_week)
                )
        else:
            response = GetMeResponse(
                id=current_user.id,
                email=current_user.email,
                username=current_user.username,
                registration_time=current_user.created_at,
                gender=current_user.gender,
                dof=current_user.dof,
                avatar_url=current_user.avatar_url,
                contacts=None
                )
    return response

@user_router.get('/{user_id}', response_model=GetUserResponse)
async def get_user(user_id: int):
    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise user_not_exists_exception
    if user.contacts is None:
        response = GetUserResponse(
            id=user.id,
            username=user.username,
            gender=user.gender,
            dof=user.dof,
            contacts=None
            )
        return response
    if hasattr(user, 'contacts'):
        response = GetUserResponse(
            id=user.id,
            username=user.username,
            gender=user.gender,
            dof=user.dof,
            contacts=ContactsSchema(vk=user.contacts.vk,
                                    telegram=user.contacts.telegram,
                                    steam=user.contacts.steam,
                                    discord=user.contacts.discord)
            )
    else:
        response = GetUserResponse(
            id=user.id,
            username=user.username,
            gender=user.gender,
            dof=user.dof,
            contacts=None
            )
    return response

@user_router.patch('/change-credits')
async def change_users_creds(current_user: Annotated[User, Depends(get_current_user)],
                             data: UpdateCreditsRequest):
    new_credits = {}
    if data.new_username:
        user = await UserDAO.get_by_username(data.new_username)
        if user:
            raise busy_username_exception
        new_credits['username'] = data.new_username
    if data.new_password:
        new_credits['hashed_password'] = get_password_hash(data.new_password)
    if data.new_dob:
        new_credits['dof'] = data.new_dob
    
    await UserDAO.update(current_user.id, **new_credits)
    return {'status': 'успешно изменено'}
    
@user_router.get('/', response_model=GetAllUsersResponse)
async def get_all_users(rediska: Annotated[RedisController, Depends(get_redis_controller)]):
    ret = {'users': []}
    users = await UserDAO.find_all()
    for user in users:
        add = {'id': user.id,
               'username': user.username,
               'avatar_url': await get_cached_avatar_url(user.id, rediska)}
        ret['users'].append(add)
    
    return ret

# @user_router.patch('/{user_id}/change-password', response_model=OnlyStatusResponse)
# async def change_password(user_id: int, new_password: str = Form(...)):
#     user = await UserDAO.get_by_id(user_id)
#     if user is None:
#         raise user_not_exists_exception
#     else:
#         await UserDAO.update(user.id, hashed_password=get_password_hash(new_password))
#         return {'status': 'password has been changed'}
    
@user_router.patch('/update-me-contacts', response_model=OnlyStatusResponse)
async def update_me_contacts(current_user: Annotated[User, Depends(get_current_user)],
                             data: UpdateMeContactsRequest):
    await UserDAO.update_contacts(current_user.id, data.model_dump())
    
    return {'status': 'good'}
    
@user_router.patch('/update-me', response_model=OnlyStatusResponse)
async def update_me(current_user: Annotated[User, Depends(get_current_user)],
                    data: UpdateCurrentUserRequest):
    await UserDAO.update_user_info(current_user.id, data.model_dump())
    return {'status': 'good'}

@user_router.patch('/update-me-avatar', response_model=OnlyStatusResponse)
async def update_avatar(current_user: Annotated[User, Depends(get_current_user)],
                        new_avatar: UploadFile | None = File(None)):
    if new_avatar is not None:
        file_url = upload_file_to_s3(new_avatar, S3_MEDIA_BUCKET)
        await UserDAO.update(current_user.id, avatar_url=file_url)
    
    return {'status': 'good'}

@user_router.get('/{user_id}/get-avatar', response_model=GetAvatarResponse)
async def get_avatar(user_id: int, rediska: Annotated[RedisController, Depends(get_redis_controller)]):
    user = await UserDAO.get_by_id(int(user_id))
    if user is None:
        raise user_not_exists_exception
    else:
        if user.avatar_url is not None:
            avatar_url = await get_cached_avatar_url(user.id, rediska, url=user.avatar_url)
            return {'avatar_url': f'{avatar_url}'}
        else:
            return {'avatar_url': 'no avatar'}

@user_router.post('/{user_id}/follow', response_model=OnlyStatusResponse)
async def follow_user(user_id: int, current_user: User = Depends(get_current_user)):
    is_followed = await UserFollowDAO.check_follow(current_user.id, user_id)
    if current_user.id == user_id:
        raise self_follow_exception
    if is_followed:
        raise already_followed_exception

    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise user_not_exists_exception
    
    await UserFollowDAO.follow(current_user.id, user_id)
    
    return {'status': 'Подписка успешна'}

@user_router.delete('/{user_id}/unfollow', response_model=OnlyStatusResponse)
async def unfollow_user(user_id: int, current_user: User = Depends(get_current_user)):
    is_followed = await UserFollowDAO.check_follow(current_user.id, user_id)
    
    if not is_followed:
        raise not_followed_exception
    else:
        await UserFollowDAO.unfollow(current_user.id, user_id)
        return {'status': 'Вы отписались'}

@user_router.get('/{user_id}/followers', response_model=GetFollowersResponse)
async def get_followers(user_id: int):
    u_followings = await UserFollowDAO.find_followers(user_id=user_id)
    
    ret = {'users': []}

    for follow in u_followings:
        ret['users'].append({'id': follow.follower.id,
                             'username': follow.follower.username})
    
    return ret

@user_router.get('/{user_id}/following', response_model=GetFollowingsResponse)
async def get_followings(user_id: int):
    u_followings = await UserFollowDAO.find_follows(user_id=user_id)
    c_followings = await CommunityMembershipDAO.get_all_users_communities(user_id)
    
    ret = {'users': [],
           'communities': []}
    if u_followings != []:
        for follow in u_followings:
            ret['users'].append({'id': follow.followed.id,
                                'username': follow.followed.username})
    if c_followings != []:
        for follow in c_followings:
            comm = await CommunityDAO.get_by_id(follow.community_id)
            ret['communities'].append({'id': follow.community_id,
                                    'name': comm.name})
    
    return ret
