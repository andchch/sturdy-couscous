import re
from datetime import date
from pydantic import EmailStr, field_validator
from sqlmodel import Field

from api.database import Base

# TODO: Check everything :)


class RoleBase(Base):
    id: int = Field(primary_key=True)


class Role(RoleBase, table=True):
    name: str = Field(default='User', unique=True)


class UserRole(RoleBase, table=True):
    name: str = Field(foreign_key='roles.name')
    user_id: int = Field(index=True, foreign_key='users.id')


class UserBase(Base):
    id: int | None = Field(index=True, primary_key=True)
    username: str = Field(
        default='JohnDoe', index=True, unique=True, nullable=False
    )

    phone_number: str
    first_name: str = Field(str, min_length=3)
    last_name: str = Field(str, min_length=3)
    email: EmailStr | None = Field(..., description="User's email")
    date_of_birth: date

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError(
                'Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр'
            )
        return value

    @field_validator('date_of_birth')
    def validate_date_of_birth(cls, value):
        if value and value >= date.today():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value


class User(UserBase, table=True):
    id: int = Field(index=True, primary_key=True)
    hashed_password: str = Field(unique=True)


class UserCreate(UserBase):
    password: str
