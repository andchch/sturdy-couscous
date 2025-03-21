from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from .models_sql import User, UserRating
from .enums import RatingEnum

class RatingService:
    def __init__(self, db: Session):
        self.db = db
    
    def rate_user(self, rater: User, rated: User, rating: RatingEnum, comment: Optional[str] = None) -> UserRating:
        """Создает новую оценку пользователя"""
        # Проверяем, не оценивал ли уже пользователь
        existing_rating = self.db.query(UserRating).filter(
            UserRating.rater_id == rater.id,
            UserRating.rated_id == rated.id
        ).first()
        
        if existing_rating:
            # Обновляем существующую оценку
            existing_rating.rating = rating
            existing_rating.comment = comment
            existing_rating.created_at = datetime.utcnow()
            return existing_rating
        
        # Создаем новую оценку
        new_rating = UserRating(
            rater_id=rater.id,
            rated_id=rated.id,
            rating=rating,
            comment=comment
        )
        self.db.add(new_rating)
        self.db.commit()
        self.db.refresh(new_rating)
        return new_rating
    
    def get_user_rating(self, user: User) -> float:
        """Получает средний рейтинг пользователя"""
        result = self.db.query(func.avg(UserRating.rating)).filter(
            UserRating.rated_id == user.id
        ).scalar()
        
        return float(result) if result is not None else 0.0
    
    def get_user_ratings(self, user: User) -> List[UserRating]:
        """Получает все оценки пользователя"""
        return self.db.query(UserRating).filter(
            UserRating.rated_id == user.id
        ).order_by(UserRating.created_at.desc()).all()
    
    def get_rating_count(self, user: User) -> int:
        """Получает количество оценок пользователя"""
        return self.db.query(UserRating).filter(
            UserRating.rated_id == user.id
        ).count()
    
    def get_rating_stats(self, user: User) -> dict:
        """Получает статистику оценок пользователя"""
        ratings = self.get_user_ratings(user)
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
    
    def get_recent_ratings(self, user: User, limit: int = 5) -> List[UserRating]:
        """Получает последние оценки пользователя"""
        return self.db.query(UserRating).filter(
            UserRating.rated_id == user.id
        ).order_by(UserRating.created_at.desc()).limit(limit).all()
    
    def get_ratings_by_user(self, user: User) -> List[UserRating]:
        """Получает все оценки, которые пользователь дал другим"""
        return self.db.query(UserRating).filter(
            UserRating.rater_id == user.id
        ).order_by(UserRating.created_at.desc()).all() 