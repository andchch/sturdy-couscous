# from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_csrf_protect import CsrfProtect

from backend.api_v1.users.router import user_router
# from api_v1.auth.router import auth_router


# TODO: Set up CORS
origins = [
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    '*']

# TODO: Set up DB creation on startup
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#     print('Database is ready')
#     yield
#     await delete_tables()
#     print('Database is cleared')
    
app = FastAPI(title='Gamers social network')
# app = FastAPI(title='Gamers social network', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

# TODO: Set up CSRF protection
# csrf = CsrfProtect(api, api.secret_key)

# app.include_router(auth_router)
app.include_router(user_router)
