from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api_v1.users.dependencies import get_current_user, get_db
from backend.api_v1.users.models_sql import User
from backend.api_v1.users.schemas import (
    RecommendationResponse,
    TopRatedRecommendationResponse,
    RecommendationSummaryResponse,
)
from backend.api_v1.recom_sys.recommendation_service import RecommendationService

recommendation_router = APIRouter(prefix='/recommendations', tags=['Recommendations'])

@recommendation_router.get('/', response_model=List[RecommendationResponse])
async def get_recommendations(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    min_rating: float = 0.0
):
    """Получает рекомендации с учетом рейтингов пользователей"""
    async with db.begin():
        recommendation_service = RecommendationService(db)
        recommendations = await recommendation_service.get_recommendations_with_ratings(
            user=current_user,
            limit=limit,
            min_rating=min_rating
        )
        return recommendations

@recommendation_router.get('/top-rated', response_model=List[TopRatedRecommendationResponse])
async def get_top_rated_recommendations(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    min_ratings: int = 5
):
    """Получает рекомендации среди пользователей с высоким рейтингом"""
    recommendation_service = RecommendationService(db)
    recommendations = await recommendation_service.get_top_rated_recommendations(
        user=current_user,
        limit=limit,
        min_ratings=min_ratings
    )
    return recommendations

@recommendation_router.get('/summary', response_model=RecommendationSummaryResponse)
async def get_recommendation_summary(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    """Получает полную сводку по рекомендациям и рейтингу пользователя"""
    recommendation_service = RecommendationService(db)
    summary = await recommendation_service.get_recommendation_summary(current_user.id)
    if not summary:
        raise HTTPException(status_code=404, detail='User not found')
    return summary 