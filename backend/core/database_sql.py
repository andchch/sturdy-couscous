from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from backend.core.config import get_db_uri

# from core.config import get_db_uri # for alembic

DATABASE_URI = get_db_uri()
# TODO: Delete on prod
DATABASE_URI = 'sqlite+aiosqlite:///db.sqlite'

async_engine = create_async_engine(url=DATABASE_URI)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

unique_str = Annotated[str, mapped_column(unique=True)]
idx_str = Annotated[str, mapped_column(unique=True, index=True)]
not_uniuq_idx_str = Annotated[int, mapped_column(nullable=False, index=True)]
not_null_str = Annotated[str, mapped_column(nullable=False)]
weight = Annotated[float, mapped_column(default=0.2)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        tablename = ''
        modified_string = list(map(lambda x: '_' + x if x.isupper() else x, self.__name__))
        split_string = ''.join(modified_string).split('_')
        split_string = list(filter(lambda x: x != '', split_string))
        for word in split_string:
            tablename += word + '_'
        return f'{tablename[:-1].lower()}s'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=datetime.now)
    