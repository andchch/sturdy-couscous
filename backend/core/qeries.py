from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from api_v1.users.models_sql import User, UserProfile

# Функция для извлечения пользователя по ID
async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User)
        .options(joinedload(User.profile))  # Подгружаем профиль пользователя
        .filter(User.id == user_id)
    )
    user = result.scalars().first()
    return user

# Функция для извлечения всех пользователей
async def get_all_users(session: AsyncSession):
    result = await session.execute(
        select(User)
        .options(joinedload(User.profile), joinedload(User.profile.weights))  # Подгружаем профиль и веса
    )
    users = result.scalars().all()
    return users

# Функция для извлечения взаимодействий пользователя
async def get_user_interactions(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(UserProfile)
        .options(joinedload(UserProfile.interactions_as_user_1), joinedload(UserProfile.interactions_as_user_2))
        .filter(UserProfile.user_id == user_id)
    )
    user_profile = result.scalars().first()
    return user_profile.interactions_as_user_1 + user_profile.interactions_as_user_2  # Все взаимодействия

# Пример вызова данных о пользователе
async def fetch_user_data(session: AsyncSession, user_id: int):
    user = await get_user_by_id(session, user_id)
    if user:
        print(f'Username: {user.username}, Email: {user.email}')
        if user.profile:
            print(f'Purpose: {user.profile.purpose}, Self-assessment Level: {user.profile.self_ass_lvl}')
            print(f'Preferred Communication: {user.profile.preferred_communication}')
        if user.profile.weights:
            print(f'Purpose Weight: {user.profile.weights.purpose_weight}')
    return user

# Пример вызова взаимодействий пользователя
async def fetch_user_interactions(session: AsyncSession, user_id: int):
    interactions = await get_user_interactions(session, user_id)
    for interaction in interactions:
        print(f'Game: {interaction.game}, User 1 Rating: {interaction.user_1_rating}, User 2 Rating: {interaction.user_2_rating}')
    return interactions
