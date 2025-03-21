from typing import Annotated
from zoneinfo import available_timezones

from fastapi import APIRouter, Depends, File, UploadFile

from backend.api_v1.auth.auth import get_password_hash
from backend.api_v1.users.dao import UserDAO, UserFollowDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User
from backend.api_v1.users.schemas import (
    ChangePasswordRequest,
    ContactsSchema,
    CreateSurveyRequest,
    CreateUserRequest,
    StatusResponse,
    GetAvatarResponse,
    GetFollowersResponse,
    GetMeResponse,
    GetUserResponse,
    OnlyStatusResponse,
    UpdateCreditsRequest,
    UpdateCurrentUserRequest,
    UpdateContactsRequest,
    UserInfoScheme, 
    UpdateDescriptionsRequest, 
    GetTimezonesResponse,
    GetFollowingsResponse
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
    avatar_file_exception,
)

user_router = APIRouter(prefix='/user', tags=['Users management'])
S3_MEDIA_BUCKET='user.media'


@user_router.post('/register', response_model=StatusResponse,
                  description="Register a new user\n\n'gender' может быть только: 'MALE' или 'FEMALE'")
async def register_user(data: CreateUserRequest):
    data = data.model_dump()
    pot_user = await UserDAO.find_all(email=data['email'])
    if not pot_user:
        pot_user = await UserDAO.find_all(username=data['username'])
    if pot_user:
        raise user_exists_exception
    
    new_user = await UserDAO.create(
        username=data['username'],
        email=data['email'],
        hashed_password=get_password_hash(data['password']),
        gender=data['gender'],
        dob=data['dob'],
        timezone=data['timezone']
    )
    response = StatusResponse(status=True,
                              info=f'User {new_user.username} created successfully')
    return response


@user_router.get('/timezones', response_model=GetTimezonesResponse)
def get_timezones():
    return {'timezones': sorted(available_timezones())}


@user_router.get('/me', response_model=GetMeResponse)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.avatar_url:
        avata = 'no avatar'
    else:
        avata = current_user.avatar_url
        
    if current_user.contacts:
        user_contacts = current_user.contacts
        user_contacts = ContactsSchema(telegram=user_contacts.telegram,
                                       steam=user_contacts.steam,
                                       discord=user_contacts.discord)
    else:
        user_contacts = None

    if current_user.info:
        user_info = current_user.info
        user_info = UserInfoScheme(purpose=user_info.purpose,
                                   preferred_communication=user_info.preferred_communication,
                                   hours_per_week=user_info.hours_per_week)
    else:
        user_info = None

    response = GetMeResponse(id=current_user.id,
                             email=current_user.email,
                             username=current_user.username,
                             registration_time=current_user.created_at,
                             gender=current_user.gender,
                             dob=current_user.dob,
                             avatar_url=avata,
                             contacts=user_contacts,
                             info=user_info)
    return response


@user_router.get('/{user_id}', response_model=GetUserResponse)
async def get_user(user_id: int):
    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise user_not_exists_exception
    if user.contacts:
        user_contacts = user.contacts
        user_contacts = ContactsSchema(telegram=user_contacts.telegram,
                                       steam=user_contacts.steam,
                                       discord=user_contacts.discord)
    else:
        user_contacts = None

    response = GetUserResponse(id=user.id,
                                username=user.username,
                                gender=user.gender,
                                dof=user.dob,
                                contacts=user_contacts)

    return response


@user_router.patch('/credits', response_model=StatusResponse)
async def change_users_creds(current_user: Annotated[User, Depends(get_current_user)],
                             data: UpdateCreditsRequest):
    new_credits = {}
    if data.new_username:
        user = await UserDAO.get_by_username(data.new_username)
        if user:
            raise busy_username_exception
        new_credits['username'] = data.new_username
    if data.new_dob:
        new_credits['dob'] = data.new_dob

    updated_user = await UserDAO.update(current_user.id, **new_credits)
    return {'status': True,
            'info' : f'User {updated_user.id} has been updated.'}


@user_router.post('/survey')
async def create_survey(current_user: Annotated[User, Depends(get_current_user)],
                        data: CreateSurveyRequest):
    """Еще не готово"""
    await UserDAO.create_survey(current_user.id, data.model_dump())
    return {'status': True,
            'info': f'Survey for user {current_user.id} created successfully'}
    
    
@user_router.patch('/change_password', response_model=StatusResponse)
async def change_password(current_user: Annotated[User, Depends(get_current_user)],
                         data: ChangePasswordRequest):
    new_credits = {}
    if data.new_password:
        new_credits['hashed_password'] = get_password_hash(data.new_password)

    updated_user = await UserDAO.update(current_user.id, **new_credits)
    return {'status': True,
            'info' : f'User password for {updated_user.id} has been updated.'}
    

@user_router.patch('/contacts', response_model=StatusResponse)
async def update_me_contacts(current_user: Annotated[User, Depends(get_current_user)],
                             data: UpdateContactsRequest):
    new_contacts = {}
    if data.telegram:
        new_contacts['telegram'] = data.telegram
    if data.steam:
        new_contacts['steam'] = data.steam
    if data.discord:
        new_contacts['discord'] = data.discord
        
    updated_contacts = await UserDAO.update_contacts(current_user.id, new_contacts)
    if updated_contacts is None:
        raise user_not_exists_exception

    return {'status': True,
            'info': f'Contacts for user {updated_contacts.user_id} updated successfully'}


@user_router.patch('/update', response_model=StatusResponse,
                   description="'gender' может быть только: 'MALE' или 'FEMALE'\n\n "
                               "'purpose' может быть только: 'FUN' или 'RESULT'")
async def update_me(current_user: Annotated[User, Depends(get_current_user)],
                    data: UpdateCurrentUserRequest):
    await UserDAO.update_user_info(current_user.id, data.model_dump())
    return {'status': True,
            'info': f'User {current_user.id} updated successfully'}


@user_router.patch('/description', response_model=StatusResponse)
async def update_description(current_user: Annotated[User, Depends(get_current_user)],
                             data: UpdateDescriptionsRequest):
    await UserDAO.update(current_user.id, **data.model_dump())

    return {'status': True,
            'info': f'User {current_user.id} updated description successfully'}


@user_router.patch('/avatar', response_model=StatusResponse)
async def update_avatar(current_user: Annotated[User, Depends(get_current_user)],
                        new_avatar: UploadFile | None = File(None)):
    if new_avatar.filename != '':
        file_url = upload_file_to_s3(new_avatar, S3_MEDIA_BUCKET)
        await UserDAO.update(current_user.id, avatar_url=file_url)
    else:
        raise avatar_file_exception
    return {'status': True,
            'info': f'User {current_user.id} updated avatar successfully'}


@user_router.get('/{user_id}/avatar', response_model=GetAvatarResponse)
async def get_avatar(user_id: int, rediska: Annotated[RedisController, Depends(get_redis_controller)]):
    user = await UserDAO.get_by_id(user_id)
    if user is None:
        raise user_not_exists_exception
    else:
        avatar_url = await get_cached_avatar_url(user.id, rediska, url=user.avatar_url)
        return {'avatar_url': f'{avatar_url}'}


@user_router.post('/{user_id}/follow', response_model=OnlyStatusResponse, description='NOT TESTES')
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


@user_router.delete('/{user_id}/unfollow', response_model=OnlyStatusResponse, description='NOT TESTES')
async def unfollow_user(user_id: int, current_user: User = Depends(get_current_user)):
    is_followed = await UserFollowDAO.check_follow(current_user.id, user_id)
    
    if not is_followed:
        raise not_followed_exception
    else:
        await UserFollowDAO.unfollow(current_user.id, user_id)
        return {'status': 'Вы отписались'}


# TODO: Проверить эндпоинты, связанные с подпиской и их схемы
@user_router.get('/{user_id}/followers', response_model=GetFollowersResponse, description='NOT TESTES')
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
    
    ret = {'users': []}
    if u_followings != []:
        for follow in u_followings:
            ret['users'].append({'id': follow.followed.id,
                                'username': follow.followed.username})
    
    return ret