from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.recommendation_system.rs import UserProfile, find_similar_users, users2
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User


rs_router = APIRouter(prefix='/rs', tags=['RS management'])


# @rs_router.get('/find')
# async def find_tm(current_user: Annotated[User, Depends(get_current_user)]):
#     # users: list[UserProfile]
#     curr_user = UserProfile(current_user.id, ['RPG', 'Action'], None,
#                             current_user.hours_per_week, None, current_user.self_assessment_lvl,
#                             ['Xbox'],
#                             current_user.purpose, current_user.username)
#     # async with async_session() as session:
#     #     query = select(User).where(User.id != curr_user.id)
#     #     result = await session.execute(query)
#     # result = result.scalar_one_or_none()
#     # for user in result:
#     #     users.append(UserProfile(user.id, user.preferred_genres, user.hours_per_week,
#     #                              user.self_assessment_lvl, user.preferred_platforms,
#     #                              user.purpose))
#     output = find_similar_users(curr_user, users2)
#     print(output)
#     out_users = []
#     for id, score in output:
#         print(f'id: {id}')
#         user = users2[id]
#         out_users.append({'username': user.username, 'score': float(score)})
#     return out_users
