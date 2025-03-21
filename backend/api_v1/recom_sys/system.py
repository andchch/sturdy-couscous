from datetime import datetime
from typing import List, Tuple
from dataclasses import dataclass
from zoneinfo import ZoneInfo
from functools import lru_cache

from sqlalchemy.orm import Session, joinedload

from backend.api_v1.users.enums import CommunicationTypeEnum
from backend.api_v1.users.models_sql import User, UserInfo


@dataclass
class UserCompatibility:
    user: User
    score: float
    matching_factors: List[str]

class RecommendationSystem:
    def __init__(self, db: Session):
        self.db = db
        
    def _calculate_age_difference(self, user1: User, user2: User) -> float:
        """Рассчитывает разницу в возрасте между пользователями"""
        if not user1.dob or not user2.dob:
            return 0.0
            
        age1 = (datetime.now() - user1.dob).days / 365.25
        age2 = (datetime.now() - user2.dob).days / 365.25
        return abs(age1 - age2)
    
    def _calculate_timezone_difference(self, user1: User, user2: User) -> float:
        """Рассчитывает разницу в часовых поясах"""
        if not user1.timezone or not user2.timezone:
            return 0.0
            
        tz1 = ZoneInfo(user1.timezone)
        tz2 = ZoneInfo(user2.timezone)
        return abs(tz1.utcoffset(datetime.now()) - tz2.utcoffset(datetime.now())).total_seconds() / 3600
    
    @lru_cache(maxsize=1000)
    def _calculate_genre_similarity(self, user1_id: int, user2_id: int) -> float:
        """Рассчитывает схожесть по жанрам"""
        genres1 = set(genre.name for genre in self.db.query(UserInfo).filter(UserInfo.user_id == user1_id).all())
        genres2 = set(genre.name for genre in self.db.query(UserInfo).filter(UserInfo.user_id == user2_id).all())
        
        if not genres1 or not genres2:
            return 0.0
            
        intersection = len(genres1.intersection(genres2))
        union = len(genres1.union(genres2))
        return intersection / union if union > 0 else 0.0
    
    def _calculate_game_similarity(self, user1: User, user2: User) -> float:
        """Рассчитывает схожесть по играм и времени в них"""
        games1 = {game.game_name: game.playtime_hours for game in user1.game_playtimes}
        games2 = {game.game_name: game.playtime_hours for game in user2.game_playtimes}
        
        if not games1 or not games2:
            return 0.0
            
        common_games = set(games1.keys()).intersection(set(games2.keys()))
        if not common_games:
            return 0.0
            
        total_similarity = 0.0
        for game in common_games:
            # Нормализуем время игры для каждого пользователя
            time1 = games1[game] / sum(games1.values())
            time2 = games2[game] / sum(games2.values())
            total_similarity += 1 - abs(time1 - time2)
            
        return total_similarity / len(common_games)
    
    def _calculate_preferences_similarity(self, info1: UserInfo, info2: UserInfo) -> Tuple[float, List[str]]:
        """Рассчитывает схожесть по предпочтениям"""
        score = 0.0
        matching_factors = []
        
        # Проверяем совпадение по цели
        if info1.purpose and info2.purpose and info1.purpose == info2.purpose:
            score += 1.0
            matching_factors.append('Цель игры')
            
        # Проверяем совпадение по формату общения
        if info1.preferred_communication and info2.preferred_communication:
            if info1.preferred_communication == info2.preferred_communication:
                score += 1.0
                matching_factors.append('Формат общения')
            elif info1.preferred_communication == CommunicationTypeEnum.INDIFFERENT or \
                 info2.preferred_communication == CommunicationTypeEnum.INDIFFERENT:
                score += 0.5
                matching_factors.append('Формат общения (один из пользователей не имеет предпочтений)')
                
        # Проверяем совпадение по дням
        if info1.preferred_days and info2.preferred_days and info1.preferred_days == info2.preferred_days:
            score += 1.0
            matching_factors.append('Предпочтительные дни')
            
        # Проверяем совпадение по времени суток
        if info1.preferred_time and info2.preferred_time and info1.preferred_time == info2.preferred_time:
            score += 1.0
            matching_factors.append('Предпочтительное время')
            
        # Нормализуем количество часов в неделю
        if info1.hours_per_week and info2.hours_per_week:
            hours_diff = abs(info1.hours_per_week - info2.hours_per_week)
            max_hours = max(info1.hours_per_week, info2.hours_per_week)
            if max_hours > 0:
                hours_similarity = 1 - (hours_diff / max_hours)
                score += hours_similarity
                matching_factors.append('Количество часов в неделю')
                
        return score / 4, matching_factors  # Нормализуем по максимальному количеству факторов
    
    def get_recommendations(self, user: User, limit: int = 10) -> List[UserCompatibility]:
        # Используем подзапросы для оптимизации
        other_users = self.db.query(User).filter(
            User.id != user.id
        ).options(
            joinedload(User.preferred_genres),
            joinedload(User.game_playtimes),
            joinedload(User.info)
        ).all()
        
        recommendations = []
        for other_user in other_users:
            # Рассчитываем общий скор совместимости
            age_diff = self._calculate_age_difference(user, other_user)
            timezone_diff = self._calculate_timezone_difference(user, other_user)
            genre_similarity = self._calculate_genre_similarity(user.id, other_user.id)
            game_similarity = self._calculate_game_similarity(user, other_user)
            
            # Получаем схожесть по предпочтениям
            preferences_score, matching_factors = self._calculate_preferences_similarity(
                user.info, other_user.info
            )
            
            # Рассчитываем итоговый скор
            # Нормализуем разницу в возрасте (максимальная разница 20 лет)
            age_score = max(0, 1 - (age_diff / 20))
            # Нормализуем разницу в часовых поясах (максимальная разница 12 часов)
            timezone_score = max(0, 1 - (timezone_diff / 12))
            
            # Взвешиваем факторы
            final_score = (
                age_score * 0.2 +
                timezone_score * 0.2 +
                genre_similarity * 0.2 +
                game_similarity * 0.2 +
                preferences_score * 0.2
            )
            
            recommendations.append(UserCompatibility(
                user=other_user,
                score=final_score,
                matching_factors=matching_factors
            ))
        
        # Сортируем по скору и возвращаем топ-N рекомендаций
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]
    