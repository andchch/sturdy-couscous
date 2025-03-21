from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api_v1.users.models_sql import User, UserInfo, GamePlaytime


@dataclass
class UserCompatibility:
    user: User
    score: float
    matching_factors: List[str]

class RecommendationSystem:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_recommendations(self, user: User, limit: int = 10) -> List[Dict]:
        """Получает рекомендации для пользователя"""
        # Получаем всех пользователей, исключая текущего
        stmt = select(User).where(User.id != user.id)
        result = await self.db.execute(stmt)
        all_users = result.scalars().all()
        
        # Рассчитываем совместимость с каждым пользователем
        recommendations = []
        for other_user in all_users:
            compatibility = await self.calculate_compatibility(user, other_user)
            if compatibility['total_score'] > 0:
                recommendations.append({
                    'user': {
                        'id': other_user.id,
                        'username': other_user.username,
                        'avatar_url': other_user.avatar_url,
                        'gender': other_user.gender,
                        'dob': other_user.dob.isoformat() if other_user.dob else None
                    },
                    'compatibility_score': compatibility['total_score'],
                    'matching_factors': compatibility['matching_factors']
                })
        
        # Сортируем по скору совместимости
        recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        return recommendations[:limit]
    
    async def calculate_compatibility(self, user1: User, user2: User) -> Dict:
        """Рассчитывает совместимость между двумя пользователями"""
        matching_factors = []
        total_score = 0.0
        
        # 1. Разница в возрасте (20%)
        age_score = await self._calculate_age_compatibility(user1, user2)
        if age_score > 0:
            matching_factors.append('age')
        total_score += age_score * 0.2
        
        # 2. Разница в часовом поясе (20%)
        timezone_score = await self._calculate_timezone_compatibility(user1, user2)
        if timezone_score > 0:
            matching_factors.append('timezone')
        total_score += timezone_score * 0.2
        
        # 3. Совпадение жанров (20%)
        genre_score = await self._calculate_genre_compatibility(user1, user2)
        if genre_score > 0:
            matching_factors.append('genres')
        total_score += genre_score * 0.2
        
        # 4. Совпадение игр (20%)
        game_score = await self._calculate_game_compatibility(user1, user2)
        if game_score > 0:
            matching_factors.append('games')
        total_score += game_score * 0.2
        
        # 5. Совпадение предпочтений (20%)
        preferences_score = await self._calculate_preferences_compatibility(user1, user2)
        if preferences_score > 0:
            matching_factors.append('preferences')
        total_score += preferences_score * 0.2
        
        return {
            'total_score': total_score,
            'matching_factors': matching_factors
        }
    
    async def _calculate_age_compatibility(self, user1: User, user2: User) -> float:
        """Рассчитывает совместимость по возрасту"""
        if not user1.dob or not user2.dob:
            return 0.0
            
        age1 = (datetime.utcnow() - user1.dob).days / 365
        age2 = (datetime.utcnow() - user2.dob).days / 365
        age_diff = abs(age1 - age2)
        
        # Максимальная разница в возрасте - 10 лет
        if age_diff > 10:
            return 0.0
            
        return 1.0 - (age_diff / 10)
    
    async def _calculate_timezone_compatibility(self, user1: User, user2: User) -> float:
        """Рассчитывает совместимость по часовому поясу"""
        if not user1.timezone or not user2.timezone:
            return 0.0
            
        # Получаем разницу в часах между часовыми поясами
        tz1 = int(user1.timezone.split(':')[0])
        tz2 = int(user2.timezone.split(':')[0])
        tz_diff = abs(tz1 - tz2)
        
        # Максимальная разница - 12 часов
        if tz_diff > 12:
            return 0.0
            
        return 1.0 - (tz_diff / 12)
    
    async def _calculate_genre_compatibility(self, user1: User, user2: User) -> float:
        """Рассчитывает совместимость по жанрам"""
        # Используем связь preferred_genres напрямую из модели User
        genres1 = {g.name for g in user1.preferred_genres}
        genres2 = {g.name for g in user2.preferred_genres}
        
        if not genres1 or not genres2:
            return 0.0
            
        # Рассчитываем пересечение жанров
        common_genres = genres1.intersection(genres2)
        total_genres = genres1.union(genres2)
        
        return len(common_genres) / len(total_genres) if total_genres else 0.0
    
    async def _calculate_game_compatibility(self, user1: User, user2: User) -> float:
        """Рассчитывает совместимость по играм"""
        # Получаем игры пользователей
        stmt1 = select(GamePlaytime).where(GamePlaytime.user_id == user1.id)
        stmt2 = select(GamePlaytime).where(GamePlaytime.user_id == user2.id)
        result1 = await self.db.execute(stmt1)
        result2 = await self.db.execute(stmt2)
        games1 = {g.game_name for g in result1.scalars().all()}
        games2 = {g.game_name for g in result2.scalars().all()}
        
        if not games1 or not games2:
            return 0.0
            
        # Рассчитываем пересечение игр
        common_games = games1.intersection(games2)
        total_games = games1.union(games2)
        
        return len(common_games) / len(total_games) if total_games else 0.0
    
    async def _calculate_preferences_compatibility(self, user1: User, user2: User) -> float:
        """Рассчитывает совместимость по предпочтениям"""
        # Получаем информацию о предпочтениях
        stmt1 = select(UserInfo).where(UserInfo.user_id == user1.id)
        stmt2 = select(UserInfo).where(UserInfo.user_id == user2.id)
        result1 = await self.db.execute(stmt1)
        result2 = await self.db.execute(stmt2)
        info1 = result1.scalar_one_or_none()
        info2 = result2.scalar_one_or_none()
        
        if not info1 or not info2:
            return 0.0
            
        score = 0.0
        factors = 0
        
        # Проверяем совпадение цели
        if info1.purpose and info2.purpose:
            if info1.purpose == info2.purpose:
                score += 1.0
            factors += 1
            
        # Проверяем совпадение предпочтительного способа общения
        if info1.preferred_communication and info2.preferred_communication:
            if info1.preferred_communication == info2.preferred_communication:
                score += 1.0
            factors += 1
            
        # Проверяем совпадение часов в неделю
        if info1.hours_per_week and info2.hours_per_week:
            hours_diff = abs(info1.hours_per_week - info2.hours_per_week)
            max_diff = max(info1.hours_per_week, info2.hours_per_week)
            if max_diff > 0:
                score += 1.0 - (hours_diff / max_diff)
            factors += 1
            
        return score / factors if factors > 0 else 0.0
    