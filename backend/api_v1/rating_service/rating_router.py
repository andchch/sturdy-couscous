from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api_v1.users.dependencies import get_current_user, get_db
from backend.api_v1.users.models_sql import User
from backend.api_v1.users.dao import UserDAO
from backend.api_v1.users.schemas import (
    RatingRequest,
    RatingResponse,
    RatingStatsResponse,
    RatingTrendResponse,
    RatingImpactResponse,
    TopRatedUserResponse,
    StatusResponse,
)
from backend.api_v1.rating_service.rating_service import RatingService
from backend.api_v1.users.exceptions import user_not_exists_exception

rating_router = APIRouter(prefix='/ratings', tags=['Ratings'])

@rating_router.post('/{user_id}/rate', response_model=StatusResponse)
async def rate_user(
    user_id: int,
    rating_data: RatingRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    """Оценивает пользователя"""
    async with db.begin():
        if current_user.id == user_id:
            raise HTTPException(status_code=400, detail='Cannot rate yourself')
            
        rated_user = await UserDAO.get_by_id(user_id)
        if not rated_user:
            raise user_not_exists_exception
            
        rating_service = RatingService(db)
        await rating_service.rate_user(
            current_user, 
            rated_user, 
            rating_data.rating, 
            rating_data.comment
        )
        
        return {
            'status': True,
            'info': f'User {user_id} rated successfully'
        }

@rating_router.get('/{user_id}/stats', response_model=RatingStatsResponse)
async def get_user_ratings(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получает статистику оценок пользователя"""
    async with db.begin():
        user = await UserDAO.get_by_id(user_id)
        if not user:
            raise user_not_exists_exception
            
        rating_service = RatingService(db)
        stats = await rating_service.get_rating_stats(user)
        return stats

@rating_router.get('/{user_id}/recent', response_model=List[RatingResponse])
async def get_recent_ratings(
    user_id: int,
    limit: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """Получает последние оценки пользователя"""
    async with db.begin():
        user = await UserDAO.get_by_id(user_id)
        if not user:
            raise user_not_exists_exception
            
        rating_service = RatingService(db)
        ratings = await rating_service.get_recent_ratings(user, limit)
        
        return [
            RatingResponse(
                rating=rating.rating.value,
                comment=rating.comment,
                from_user=rating.rater.username,
                date=rating.created_at
            )
            for rating in ratings
        ]

@rating_router.get('/top', response_model=List[TopRatedUserResponse])
async def get_top_rated_users(
    limit: int = 10,
    min_ratings: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """Получает список пользователей с наивысшим рейтингом"""
    async with db.begin():
        rating_service = RatingService(db)
        top_users = await rating_service.get_top_rated_users(limit, min_ratings)
        
        return [
            TopRatedUserResponse(
                user={
                    'id': user.id,
                    'username': user.username,
                    'avatar_url': user.avatar_url
                },
                rating=rating
            )
            for user, rating in top_users
        ]

@rating_router.get('/trend', response_model=RatingTrendResponse)
async def get_rating_trend(
    current_user: Annotated[User, Depends(get_current_user)],
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """Получает тренд рейтинга пользователя"""
    async with db.begin():
        rating_service = RatingService(db)
        trend = await rating_service.get_rating_trend(current_user, days)
        return RatingTrendResponse(trend=trend)

@rating_router.get('/impact', response_model=RatingImpactResponse)
async def get_rating_impact(
    current_user: Annotated[User, Depends(get_current_user)],
    db: AsyncSession = Depends(get_db)
):
    """Получает влияние рейтинга на рекомендации"""
    async with db.begin():
        rating_service = RatingService(db)
        impact = await rating_service.get_rating_impact(current_user)
        return RatingImpactResponse(**impact) 