from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from backend.api_v1.games.models_nosql import MinecraftModel
from backend.api_v1.users.dao import UserDAO, UserInteractionDAO
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User
from backend.core.database_mongo import MongoController
from backend.api_v1.games.models_nosql import UserGamesModel


user_router = APIRouter(prefix='/user', tags=['Users management'])


@user_router.post('/register')
async def create_user(username: str, email: str, password: str, file: Annotated[bytes, File()]):
    # if not file.file.content_type.startswith('image/'):
    #     raise HTTPException(status_code=400, detail='Invalid file type. Please upload an image.')
    try:
        avatar_data = file
        new_user = await UserDAO.create(
            username=username,
            email=email,
            hashed_password=password,
            avatar=avatar_data,
            # content_type=file.file.content_type
        )
        return {'status': 'goida'}
        # return new_user
    except Exception as e:
        return {'status': str(e)}
    
    
@user_router.post('/create_user_interaction')
async def create_user_interaction(id1: int, id2: int, game: str, u1r: str, u2r: str):
    try:
        new_user_int = await UserInteractionDAO.create_interaction(
            id1, id2, game, u1r, u2r
        )
        return new_user_int
    except Exception as e:
        return {'status': str(e)}
    
    
@user_router.post('/create/ugm')
async def create_ugm(hour: int):
    game = MinecraftModel(hours_played=hour)
    ugm = UserGamesModel(user_id=1, games=[game])
    mongo = MongoController()
    print(ugm.model_dump())
    await mongo.add_user_games(ugm)


@user_router.get('/me')
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
