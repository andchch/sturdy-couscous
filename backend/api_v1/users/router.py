from fastapi import APIRouter

from backend.api_v1.users.dao import UserDAO, UserInteractionDAO


user_router = APIRouter(prefix='/user', tags=['Users management'])


@user_router.post('/register')
async def register_user():
    pass


@user_router.post('/create_user')
async def create_user(username: str, email: str, password: str):
    try:
        new_user = await UserDAO.create(
            username=username,
            email=email,
            hashed_password=password
        )
        return new_user
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


@user_router.get('/me')
async def get_me():
    pass
