from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api_v1.users.dependencies import get_current_user, get_db
from backend.api_v1.users.models_sql import User
from backend.api_v1.recom_sys.schemas import RecommendationResponse
from backend.api_v1.recom_sys.system import RecommendationSystem
from sqlalchemy import select

recommendation_router = APIRouter(prefix='/recommendations', tags=['Recommendations'])

@recommendation_router.get('/', response_model=List[RecommendationResponse])
async def get_recommendations(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    game: Optional[str] = Query(None, description='Фильтр по игре'),
    purpose: Optional[str] = Query(None, description='Фильтр по цели')
):
    """Получает 5 наиболее подходящих пользователей для текущего пользователя"""
    async with db.begin():
        # Перезагружаем текущего пользователя со всеми связями
        stmt = (
            select(User)
            .where(User.id == current_user.id)
            .options(
                selectinload(User.preferred_genres),
                selectinload(User.game_playtimes),
                selectinload(User.info)
            )
        )
        result = await db.execute(stmt)
        current_user = result.scalar_one()
        
        recommendation_system = RecommendationSystem(db)
        recommendations = await recommendation_system.get_recommendations(
            user=current_user, 
            limit=5,
            game_filter=game,
            purpose_filter=purpose
        )
        return recommendations
