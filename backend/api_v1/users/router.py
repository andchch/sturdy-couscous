from fastapi import APIRouter, HTTPException, status, Depends


user_router = APIRouter(prefix='/user', tags=['Users management'])


@user_router.post('/register')
async def register_user():
    pass

@user_router.get('/me')
async def get_me():
    pass
