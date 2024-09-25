from sqlalchemy import select as sqlalchemy_select, delete as sqlalchemy_delete

from api.dao.base import BaseDAO
from api.database import async_session_maker
from api.users.models import User


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_one_or_none(
        cls, **filter_by
    ) -> User | None:  # TODO: Specify allowed filter params
        async with async_session_maker() as session:
            query = sqlalchemy_select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, user_id: int) -> int | None:
        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_select(cls.model).filter_by(id=user_id)
                result = await session.execute(query)
                user_to_delete = result.scalar_one_or_none()

                if not user_to_delete:
                    return None

                await session.execute(
                    sqlalchemy_delete(cls.model).filter_by(id=user_id)
                )

                await session.commit()
                return user_id
