from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, and_, select

from backend.api_v1.users.enums import RatingEnum
from backend.api_v1.users.models_sql import User, UserRating


class RatingService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def rate_user(self, rater: User, rated: User, rating: RatingEnum, comment: Optional[str] = None) -> UserRating:
        """Создает новую оценку пользователя"""
        # Проверяем, не оценивал ли уже пользователь
        stmt = select(UserRating).where(
            UserRating.rater_id == rater.id,
            UserRating.rated_id == rated.id
        )
        result = await self.db.execute(stmt)
        existing_rating = result.scalar_one_or_none()
        
        if existing_rating:
            # Обновляем существующую оценку
            existing_rating.rating = rating
            existing_rating.comment = comment
            existing_rating.created_at = datetime.utcnow()
            await self.db.commit()
            return existing_rating
        
        # Создаем новую оценку
        new_rating = UserRating(
            rater_id=rater.id,
            rated_id=rated.id,
            rating=rating,
            comment=comment
        )
        self.db.add(new_rating)
        await self.db.commit()
        await self.db.refresh(new_rating)
        return new_rating
    
    async def get_user_rating(self, user: User) -> float:
        """Получает средний рейтинг пользователя"""
        stmt = select(func.avg(UserRating.rating)).where(
            UserRating.rated_id == user.id
        )
        result = await self.db.execute(stmt)
        avg_rating = result.scalar()
        return float(avg_rating) if avg_rating is not None else 0.0
    
    async def get_user_ratings(self, user: User) -> List[UserRating]:
        """Получает все оценки пользователя"""
        stmt = select(UserRating).where(
            UserRating.rated_id == user.id
        ).order_by(UserRating.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_rating_count(self, user: User) -> int:
        """Получает количество оценок пользователя"""
        stmt = select(func.count(UserRating.id)).where(
            UserRating.rated_id == user.id
        )
        result = await self.db.execute(stmt)
        return result.scalar()
    
    async def get_rating_stats(self, user: User) -> dict:
        """Получает статистику оценок пользователя"""
        ratings = await self.get_user_ratings(user)
        total_ratings = len(ratings)
        
        if total_ratings == 0:
            return {
                'average_rating': 0.0,
                'total_ratings': 0,
                'rating_distribution': {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                    '5': 0
                }
            }
        
        rating_distribution = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0
        }
        
        total_score = 0
        for rating in ratings:
            rating_value = int(rating.rating.value)
            rating_distribution[str(rating_value)] += 1
            total_score += rating_value
        
        return {
            'average_rating': total_score / total_ratings,
            'total_ratings': total_ratings,
            'rating_distribution': rating_distribution
        }
    
    async def get_recent_ratings(self, user: User, limit: int = 5) -> List[UserRating]:
        """Получает последние оценки пользователя"""
        stmt = select(UserRating).where(
            UserRating.rated_id == user.id
        ).order_by(UserRating.created_at.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_ratings_by_user(self, user: User) -> List[UserRating]:
        """Получает все оценки, которые пользователь дал другим"""
        stmt = select(UserRating).where(
            UserRating.rater_id == user.id
        ).order_by(UserRating.created_at.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_rating_trend(self, user: User, days: int = 30) -> Dict[str, float]:
        """Получает тренд рейтинга за указанный период"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Получаем средний рейтинг за каждый день
        stmt = select(
            func.date(UserRating.created_at).label('date'),
            func.avg(UserRating.rating).label('avg_rating')
        ).where(
            and_(
                UserRating.rated_id == user.id,
                UserRating.created_at >= start_date
            )
        ).group_by(
            func.date(UserRating.created_at)
        )
        
        result = await self.db.execute(stmt)
        daily_ratings = result.all()
        
        # Преобразуем в словарь
        trend = {str(rating.date): float(rating.avg_rating) for rating in daily_ratings}
        return trend
    
    async def get_top_rated_users(self, limit: int = 10, min_ratings: int = 5) -> List[Tuple[User, float]]:
        """Получает список пользователей с наивысшим рейтингом"""
        # Подзапрос для подсчета количества оценок
        rating_counts = select(
            UserRating.rated_id,
            func.count(UserRating.id).label('count')
        ).group_by(UserRating.rated_id).subquery()
        
        # Основной запрос с фильтрацией по минимальному количеству оценок
        stmt = select(
            User,
            func.avg(UserRating.rating).label('avg_rating')
        ).join(
            UserRating, User.id == UserRating.rated_id
        ).join(
            rating_counts, User.id == rating_counts.c.rated_id
        ).where(
            rating_counts.c.count >= min_ratings
        ).group_by(
            User.id
        ).order_by(
            func.avg(UserRating.rating).desc()
        ).limit(limit)
        
        result = await self.db.execute(stmt)
        return [(user, float(avg_rating)) for user, avg_rating in result.all()]
    
    async def get_rating_comparison(self, user1: User, user2: User) -> Dict[str, float]:
        """Сравнивает рейтинги двух пользователей"""
        stats1 = await self.get_rating_stats(user1)
        stats2 = await self.get_rating_stats(user2)
        
        return {
            'user1': {
                'username': user1.username,
                'average_rating': stats1['average_rating'],
                'total_ratings': stats1['total_ratings']
            },
            'user2': {
                'username': user2.username,
                'average_rating': stats2['average_rating'],
                'total_ratings': stats2['total_ratings']
            },
            'rating_difference': stats1['average_rating'] - stats2['average_rating']
        }
    
    async def get_rating_impact(self, user: User) -> Dict[str, float]:
        """Рассчитывает влияние рейтинга на рекомендации"""
        # Получаем средний рейтинг
        avg_rating = await self.get_user_rating(user)
        
        # Получаем количество оценок
        rating_count = await self.get_rating_count(user)
        
        # Рассчитываем "силу" рейтинга (чем больше оценок, тем сильнее влияние)
        rating_strength = min(1.0, rating_count / 10)  # Максимальная сила при 10+ оценках
        
        return {
            'average_rating': avg_rating,
            'rating_count': rating_count,
            'rating_strength': rating_strength,
            'recommendation_boost': avg_rating * rating_strength  # Множитель для рекомендаций
        }
    
    async def get_rating_summary(self, user: User) -> Dict:
        """Получает полную сводку по рейтингу пользователя"""
        stats = await self.get_rating_stats(user)
        trend = await self.get_rating_trend(user)
        impact = await self.get_rating_impact(user)
        recent_ratings = await self.get_recent_ratings(user)
        
        return {
            'stats': stats,
            'trend': trend,
            'impact': impact,
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
        