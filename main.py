from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from core.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('Database is ready')
    yield  # Дальше - после выключения
    await delete_tables()
    print('Database is cleared')


app = FastAPI(title='Gamers social network', lifespan=lifespan)

router = APIRouter(prefix='/api')


app.include_router(router)
