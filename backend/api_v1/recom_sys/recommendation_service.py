from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api_v1.users.models_sql import User
from backend.api_v1.recom_sys.system import RecommendationSystem
from backend.api_v1.rating_service.rating_service import RatingService

class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.recommendation_system = RecommendationSystem(db)
        self.rating_service = RatingService(db)
    
    async def get_recommendations_with_ratings(
        self,
        user: User,
        limit: int = 10,
        min_rating: float = 0.0
    ) -> List[Dict]:
        """Получает рекомендации с учетом рейтингов пользователей"""
        # Получаем базовые рекомендации
        recommendations = await self.recommendation_system.get_recommendations(user, limit)
        
        # Фильтруем и обогащаем рекомендации рейтингами
        enriched_recommendations = []
        for rec in recommendations:
            # Получаем рейтинг пользователя
            rating_stats = await self.rating_service.get_rating_stats(rec['user'])
            avg_rating = rating_stats['average_rating']
            
            # Пропускаем пользователей с низким рейтингом
            if avg_rating < min_rating:
                continue
                
            # Получаем последние оценки
            recent_ratings = await self.rating_service.get_recent_ratings(rec['user'], limit=3)
            
            # Обогащаем рекомендацию
            enriched_rec = {
                'user': rec['user'],
                'compatibility_score': rec['compatibility_score'],
                'matching_factors': rec['matching_factors'],
                'rating': {
                    'average': avg_rating,
                    'total': rating_stats['total_ratings'],
                    'distribution': rating_stats['rating_distribution']
                },
                'recent_ratings': [
                    {
                        'rating': rating.rating.value,
                        'comment': rating.comment,
                        'from_user': rating.rater.username,
                        'date': rating.created_at.isoformat()
                    }
                    for rating in recent_ratings
                ]
            }
            enriched_recommendations.append(enriched_rec)
            
        return enriched_recommendations
    
    async def get_user_profile_with_stats(self, user_id: int) -> Optional[Dict]:
        """Получает профиль пользователя со статистикой"""
        # Получаем пользователя
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
            
        # Получаем статистику рейтинга
        rating_stats = await self.rating_service.get_rating_stats(user)
        rating_trend = await self.rating_service.get_rating_trend(user)
        recent_ratings = await self.rating_service.get_recent_ratings(user)
        
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'avatar_url': user.avatar_url,
                'gender': user.gender,
                'dob': user.dob.isoformat() if user.dob else None
            },
            'rating_stats': rating_stats,
            'rating_trend': rating_trend,
            'recent_ratings': [
                {
                    'rating': rating.rating.value,
                    'comment': rating.comment,
                    'from_user': rating.rater.username,
                    'date': rating.created_at.isoformat()
                }
                for rating in recent_ratings
            ]
        }
    
    async def get_top_rated_recommendations(
        self,
        user: User,
        limit: int = 10,
        min_ratings: int = 5
    ) -> List[Dict]:
        """Получает рекомендации среди пользователей с высоким рейтингом"""
        # Получаем пользователей с высоким рейтингом
        top_users = await self.rating_service.get_top_rated_users(limit, min_ratings)
        
        # Получаем рекомендации для этих пользователей
        recommendations = []
        for rated_user, rating in top_users:
            # Получаем совместимость с текущим пользователем
            compatibility = await self.recommendation_system.calculate_compatibility(user, rated_user)
            
            recommendations.append({
                'user': {
                    'id': rated_user.id,
                    'username': rated_user.username,
                    'avatar_url': rated_user.avatar_url
                },
                'compatibility_score': compatibility['total_score'],
                'matching_factors': compatibility['matching_factors'],
                'rating': {
                    'average': rating,
                    'total': await self.rating_service.get_rating_count(rated_user)
                }
            })
        
        return recommendations
    
    async def get_recommendation_summary(self, user_id: int) -> Optional[Dict]:
        """Получает полную сводку по рекомендациям и рейтингу пользователя"""
        # Получаем пользователя
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
            
        # Получаем рекомендации
        recommendations = await self.get_recommendations_with_ratings(user)
        
        # Получаем топ пользователей по рейтингу
        top_users = await self.rating_service.get_top_rated_users(limit=5)
        
        # Получаем сводку по рейтингу
        rating_summary = await self.rating_service.get_rating_summary(user)
        
        return {
            'user': {
                'id': user.id,
                'username': user.username,
                'avatar_url': user.avatar_url
            },
            'recommendations': recommendations,
            'rating_summary': rating_summary,
            'top_rated_users': [
                {
                    'user': {
                        'id': rated_user.id,
                        'username': rated_user.username,
                        'avatar_url': rated_user.avatar_url
                    },
                    'rating': rating
                }
                for rated_user, rating in top_users
            ]
        } 