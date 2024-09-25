# from contextlib import asynccontextmanager
from fastapi import FastAPI
# from fastapi_csrf_protect import CsrfProtect

from api.users.router import router as router_users
from api.auth.router import router as router_auth


"""@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('Database is ready')
    yield
    await delete_tables()
    print('Database is cleared')"""


app = FastAPI(title='Gamers social network')
# app = FastAPI(title='Gamers social network', lifespan=lifespan)

# csrf = CsrfProtect(api, api.secret_key)

app.include_router(router_auth)
app.include_router(router_users)
