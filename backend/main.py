# from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi_csrf_protect import CsrfProtect

from backend.admin import create_admin
from backend.api_v1.users.router import user_router
from backend.api_v1.auth.router import auth_router
# from backend.api_v1.recommendation_system.router import rs_router
from backend.api_v1.external_integration.router import ext_integration_router
from backend.api_v1.games.router import game_router
from backend.api_v1.recom_sys.router import recommendation_router


# TODO: Set up CORS
origins = [
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    '*:3000',
    '*']

# TODO: Set up DB creation on startup
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#     print('Database is ready')
#     yield
#     await delete_tables()
#     print('Database is cleared')
    
app = FastAPI(title='Gamers social network', version='0.1.0')
create_admin(app)
# app = FastAPI(title='Gamers social network', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

# TODO: Set up CSRF protection
# csrf = CsrfProtect(api, api.secret_key)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ext_integration_router)
app.include_router(game_router)
app.include_router(recommendation_router)
# app.include_router(rating_router)
