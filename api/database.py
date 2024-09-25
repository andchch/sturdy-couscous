from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declared_attr, mapped_column
from sqlmodel import SQLModel

from api.config import get_db_url

DATABASE_URL = get_db_url()
DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite'

async_engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(SQLModel):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        tablename = ''
        modified_string = list(
            map(lambda x: '_' + x if x.isupper() else x, self.__name__)
        )
        split_string = ''.join(modified_string).split('_')
        split_string = list(filter(lambda x: x != '', split_string))
        for word in split_string:
            tablename += word + '_'
        return f'{tablename[:-1].lower()}s'

    created_at: datetime = Annotated[
        datetime, mapped_column(server_default=func.now())
    ]
    updated_at: datetime = Annotated[
        datetime,
        mapped_column(server_default=func.now(), onupdate=datetime.now),
    ]
