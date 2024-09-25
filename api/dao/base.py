from sqlalchemy import (
    select as sqlalchemy_select,
    update as sqlalchemy_update,
    delete as sqlalchemy_delete,
)
from sqlalchemy.exc import SQLAlchemyError

from api.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find(cls, number: int = None, **filter_by):
        async with async_session_maker() as session:
            if number is None:
                query = sqlalchemy_select(cls.model).filter_by(**filter_by)
            else:
                query = (
                    sqlalchemy_select(cls.model)
                    .filter_by(**filter_by)
                    .limit(number)
                )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(
                        *[
                            getattr(cls.model, k) == v
                            for k, v in filter_by.items()
                        ]
                    )
                    .values(**values)
                    .execution_options(synchronize_session='fetch')
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, **filter_by):
        if not filter_by:
            raise ValueError('At least one filter is required.')

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
