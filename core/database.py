from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite'


class BaseModel(DeclarativeBase):
    pass


async_engine = create_async_engine(url=DATABASE_URL, echo=False, future=True)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


try:
    session = get_async_session()
    print('Database connection successful')
    session.aclose()
except Exception as e:
    print(f'Database connection error: {e}')
