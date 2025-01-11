from typing import Generic, List, Optional, TypeVar

from sqlalchemy import delete, select, update

from .database_sql import Base, async_session

ModelType = TypeVar('ModelType', bound=Base)

class BaseDAO(Generic[ModelType]):
    model = None

    @classmethod
    async def get_by_id(cls, model_id: int) -> Optional[ModelType]:
        async with async_session() as session:
            return await session.get(cls.model, model_id)

    @classmethod
    async def get_all(cls) -> List[ModelType]:
        async with async_session() as session:
            result = await session.execute(select(cls.model))
            return result.scalars().all()
        
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def create(cls, **data) -> ModelType:
        async with async_session() as session:
            instance = cls.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    @classmethod
    async def update(cls, model_id: int, **data) -> Optional[ModelType]:
        async with async_session() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(**data)
            await session.execute(query)
            await session.commit()
            return await cls.get_by_id(model_id)

    @classmethod
    async def delete(cls, model_id: int) -> bool:
        async with async_session() as session:
            query = delete(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0 