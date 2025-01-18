"""
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


class UserProfile:
    def __init__(self, user_id, preferred_genres, playtime, hours_per_week,
                 preferred_days, self_ass_lvl, platforms, purpose, username):
        self.user_id = user_id
        # self.preferred_genres = preferred_genres
        # self.playtime = playtime
        self.hours_per_week = hours_per_week
        # self.preferred_days = preferred_days
        self.self_ass_lvl = self_ass_lvl
        self.platforms = platforms
        self.purpose = purpose
        self.username = username

users2 = [
    UserProfile(1, ['Action', 'RPG'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 10, ['Monday', 'Wednesday'], 'MID', ['PC'], 'FUN', 'PennyIntrospective'),
    UserProfile(2, ['RPG', 'Strategy'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 15, ['Tuesday', 'Thursday'], 'MID', ['PC'], 'RESULT', 'CatalogCherisher'),
    UserProfile(3, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Monday', 'Wednesday'], 'HIGH', ['PC', 'Xbox'], 'FUN', 'ChefMeaty'),
    UserProfile(4, ['Adventure', 'Action'], {'morning': False, 'afternoon': True, 'evening': False, 'night': True}, 8, ['Friday', 'Saturday'], 'LOW', ['PS5'], 'FUN', 'SassySnarker'),
    UserProfile(5, ['Shooter', 'Strategy'], {'morning': True, 'afternoon': True, 'evening': False, 'night': False}, 20, ['Sunday', 'Wednesday'], 'MID', ['PC'], 'RESULT', 'RadiantTrotter'),
    UserProfile(6, ['Strategy', 'RPG'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 14, ['Monday', 'Thursday'], 'HIGH', ['PC', 'PS5'], 'FUN', 'SailorRevive'),
    UserProfile(7, ['Adventure', 'Shooter'], {'morning': False, 'afternoon': False, 'evening': True, 'night': True}, 18, ['Friday', 'Sunday'], 'MID', ['PC'], 'RESULT', 'ListSubscriber'),
    UserProfile(8, ['RPG', 'Action'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Wednesday', 'Saturday'], 'LOW', ['Xbox'], 'FUN', 'GourmetExperience'),
    UserProfile(9, ['Shooter', 'Action'], {'morning': True, 'afternoon': True, 'evening': False, 'night': True}, 22, ['Monday', 'Thursday'], 'MID', ['PC', 'Xbox'], 'RESULT', 'BlossomCoach'),
    UserProfile(10, ['RPG', 'Adventure'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 16, ['Tuesday', 'Friday'], 'HIGH', ['PS5'], 'FUN', 'InspiringInnovator'),
    UserProfile(11, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 10, ['Monday', 'Wednesday'], 'MID', ['PC'], 'FUN', 'EncryptedEngineer'),
    UserProfile(12, ['RPG', 'Strategy'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 15, ['Tuesday', 'Thursday'], 'MID', ['PC'], 'RESULT', 'LimitlessSnacks'),
    UserProfile(13, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Monday', 'Wednesday'], 'HIGH', ['PC', 'Xbox'], 'FUN', 'VoicedCheerful'),
    UserProfile(14, ['Adventure', 'Action'], {'morning': False, 'afternoon': True, 'evening': False, 'night': True}, 8, ['Friday', 'Saturday'], 'LOW', ['PS5'], 'FUN', 'RusticPianist'),
    UserProfile(15, ['Shooter', 'Strategy'], {'morning': True, 'afternoon': True, 'evening': False, 'night': False}, 20, ['Sunday', 'Wednesday'], 'MID', ['PC'], 'RESULT', 'TrivialJoy'),
    UserProfile(16, ['Strategy', 'RPG'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 14, ['Monday', 'Thursday'], 'HIGH', ['PC', 'PS5'], 'FUN', 'GourmandRabbit'),
    UserProfile(17, ['Adventure', 'Shooter'], {'morning': False, 'afternoon': False, 'evening': True, 'night': True}, 18, ['Friday', 'Sunday'], 'MID', ['PC'], 'RESULT', 'BoisterousPoise'),
    UserProfile(18, ['RPG', 'Action'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Wednesday', 'Saturday'], 'LOW', ['Xbox'], 'FUN', 'DesireMatchmaker'),
    UserProfile(19, ['Shooter', 'Action'], {'morning': True, 'afternoon': True, 'evening': False, 'night': True}, 22, ['Monday', 'Thursday'], 'MID', ['PC', 'Xbox'], 'RESULT', 'SizzleBlade'),
    UserProfile(20, ['RPG', 'Adventure'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 16, ['Tuesday', 'Friday'], 'HIGH', ['PS5'], 'FUN', 'LeisureShoes'),
    UserProfile(21, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 10, ['Monday', 'Wednesday'], 'MID', ['PC'], 'FUN', 'TechnoEntity'),
    UserProfile(22, ['RPG', 'Strategy'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 15, ['Tuesday', 'Thursday'], 'MID', ['PC'], 'RESULT', 'HeroGreeter'),
    UserProfile(23, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Monday', 'Wednesday'], 'HIGH', ['PC', 'Xbox'], 'FUN', 'RoutineScar'),
    UserProfile(24, ['Adventure', 'Action'], {'morning': False, 'afternoon': True, 'evening': False, 'night': True}, 8, ['Friday', 'Saturday'], 'LOW', ['PS5'], 'FUN', 'EfficientClient'),
    UserProfile(25, ['Shooter', 'Strategy'], {'morning': True, 'afternoon': True, 'evening': False, 'night': False}, 20, ['Sunday', 'Wednesday'], 'MID', ['PC'], 'RESULT', 'FunnyElder'),
    UserProfile(26, ['Strategy', 'RPG'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 14, ['Monday', 'Thursday'], 'HIGH', ['PC', 'PS5'], 'FUN', 'ImaginedChampion'),
    UserProfile(27, ['Adventure', 'Shooter'], {'morning': False, 'afternoon': False, 'evening': True, 'night': True}, 18, ['Friday', 'Sunday'], 'MID', ['PC'], 'RESULT', 'LoggerPoet'),
    UserProfile(28, ['RPG', 'Action'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Wednesday', 'Saturday'], 'LOW', ['Xbox'], 'FUN', 'MadcapDroid'),
    UserProfile(29, ['Shooter', 'Action'], {'morning': True, 'afternoon': True, 'evening': False, 'night': True}, 22, ['Monday', 'Thursday'], 'MID', ['PC', 'Xbox'], 'RESULT', 'EuphoricInnovator'),
    UserProfile(30, ['RPG', 'Adventure'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 16, ['Tuesday', 'Friday'], 'HIGH', ['PS5'], 'FUN', 'RhythmEvent'),
    UserProfile(31, ['Action', 'RPG'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 10, ['Monday', 'Wednesday'], 'MID', ['PC'], 'FUN', 'MaverickFun'),
    UserProfile(32, ['RPG', 'Strategy'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 15, ['Tuesday', 'Thursday'], 'MID', ['PC'], 'RESULT', 'UncertainHill'),
    UserProfile(33, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Monday', 'Wednesday'], 'HIGH', ['PC', 'Xbox'], 'FUN', 'CompactAngler'),
    UserProfile(34, ['Adventure', 'Action'], {'morning': False, 'afternoon': True, 'evening': False, 'night': True}, 8, ['Friday', 'Saturday'], 'LOW', ['PS5'], 'FUN', 'AnglingBear'),
    UserProfile(35, ['Shooter', 'Strategy'], {'morning': True, 'afternoon': True, 'evening': False, 'night': False}, 20, ['Sunday', 'Wednesday'], 'MID', ['PC'], 'RESULT', 'PeppyAssassin'),
    UserProfile(36, ['Strategy', 'RPG'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 14, ['Monday', 'Thursday'], 'HIGH', ['PC', 'PS5'], 'FUN', 'SprigEndurance'),
    UserProfile(37, ['Adventure', 'Shooter'], {'morning': False, 'afternoon': False, 'evening': True, 'night': True}, 18, ['Friday', 'Sunday'], 'MID', ['PC'], 'RESULT', 'PlayfulKitty'),
    UserProfile(38, ['RPG', 'Action'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Wednesday', 'Saturday'], 'LOW', ['Xbox'], 'FUN', 'PorcelainLove'),
    UserProfile(39, ['Shooter', 'Action'], {'morning': True, 'afternoon': True, 'evening': False, 'night': True}, 22, ['Monday', 'Thursday'], 'MID', ['PC', 'Xbox'], 'RESULT', 'SugarGluttony'),
    UserProfile(40, ['RPG', 'Adventure'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 16, ['Tuesday', 'Friday'], 'HIGH', ['PS5'], 'FUN', 'AwakenedMemories'),
    UserProfile(41, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 10, ['Monday', 'Wednesday'], 'MID', ['PC'], 'FUN', 'MayflowerInfluencer'),
    UserProfile(42, ['RPG', 'Strategy'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 15, ['Tuesday', 'Thursday'], 'MID', ['PC'], 'RESULT', 'ReelerIn'),
    UserProfile(43, ['Action', 'Shooter'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Monday', 'Wednesday'], 'HIGH', ['PC', 'Xbox'], 'FUN', 'FieryPanda'),
    UserProfile(44, ['Adventure', 'Action'], {'morning': False, 'afternoon': True, 'evening': False, 'night': True}, 8, ['Friday', 'Saturday'], 'LOW', ['PS5'], 'FUN', 'MidtownJazz'),
    UserProfile(45, ['Shooter', 'Strategy'], {'morning': True, 'afternoon': True, 'evening': False, 'night': False}, 20, ['Sunday', 'Wednesday'], 'MID', ['PC'], 'RESULT', 'RhythmSmith'),
    UserProfile(46, ['Strategy', 'RPG'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 14, ['Monday', 'Thursday'], 'HIGH', ['PC', 'PS5'], 'FUN', 'KidDude'),
    UserProfile(47, ['Adventure', 'Shooter'], {'morning': False, 'afternoon': False, 'evening': True, 'night': True}, 18, ['Friday', 'Sunday'], 'MID', ['PC'], 'RESULT', 'TenaciousHero'),
    UserProfile(48, ['RPG', 'Action'], {'morning': True, 'afternoon': False, 'evening': True, 'night': False}, 12, ['Wednesday', 'Saturday'], 'LOW', ['Xbox'], 'FUN', 'VibratoCreamer'),
    UserProfile(49, ['Shooter', 'Action'], {'morning': True, 'afternoon': True, 'evening': False, 'night': True}, 22, ['Monday', 'Thursday'], 'MID', ['PC', 'Xbox'], 'RESULT', 'GrassyGrouse'),
    UserProfile(50, ['RPG', 'Adventure'], {'morning': False, 'afternoon': True, 'evening': True, 'night': False}, 16, ['Tuesday', 'Friday'], 'HIGH', ['PS5'], 'FUN', 'FeatherRaven'),
]

"""


import json
from sklearn.metrics.pairwise import cosine_similarity

from backend.api_v1.recommendation_system.calc_utils import (
    euclidean_similarity,
    jaccard_similarity,
)
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.api_v1.recommendation_system.models import UserRSProfileDAO
from backend.api_v1.recommendation_system.utilities import make_hashable
from backend.api_v1.users.dao import UserDAO, UserWeightsDAO
from backend.api_v1.users.models_sql import UserWeights
from backend.core.database_mongo import MongoController
from backend.redis.cache import RedisController


async def find_teammates(user_id: int, mongo: MongoController, redis: RedisController, top_n: int = 5):
    low_quality_flag = False
    
    # берем из кеша, если есть
    cache_key = f'teammates:{user_id}'
    cached_result = await redis.redis.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    # Получаем профиль рекомендательный профиль
    target_user = await UserRSProfileDAO.get_rs_profile_by_id(user_id)
    if not target_user:
        return {
            'info': 'No profile for this user',
            'mates': []
        }
    
    user_weights = await UserWeightsDAO.get_by_user_id(user_id)
    if not user_weights:
        low_quality_flag = True
        default = {'purpose_weight': 0.25,
                   'self_assessment_lvl_weight': 0.25,
                   'preferred_communication_weight': 0.25,
                   'hours_per_week_weight': 0.25}
        # user_weights = UserWeights(default)
        user_weights = default
    # Получаем всех остальных пользователей
    all_users = await UserRSProfileDAO.get_all_others(user_id)

    # Получаем игры пользователя и все игры
    user_games = await mongo.get_data(collection='games', steam_id=user_id)
    z = await mongo.db.games.find().to_list(length=None)
    all_users_games = { u['steam_id']: u['response']['games'] for u in z }
    all_games = list({make_hashable(game): game for games in all_users_games.values() for game in games}.values())
    
    all_users_games = {}
    for item in z:
        all_users_games[item['user_id']] = [g['name'] for g in item['response']['games']]
        # if item['user_id'] not in all_users_games.keys():
        #     all_users_games[item['user_id']] = [item['response']['games']['name']]
        # else:
        #     all_users_games[item['user_id']].append(item['response']['games']['name'])

    # tfidf_res = tfidf_similarity2({ u['steam_id']: u['response']['games'] for u in z })
    all_games_texts = [' '.join(games) for games in all_users_games.values()]
    vectorizer_games = TfidfVectorizer()
    tfidf_matrix_games = vectorizer_games.fit_transform(all_games_texts)
    
    try:
        user_index = list(all_users_games.keys()).index(user_id)
        cosine_sim_games = cosine_similarity(tfidf_matrix_games[user_index], tfidf_matrix_games).flatten()
    except ValueError:
        cosine_sim_games = 0

    
    # weights = {'purpose': user_weights.purpose_weight,
    #            'self_assessment_lvl': user_weights.self_assessment_lvl_weight,
    #            'preferred_communication': user_weights.preferred_communication_weight,
    #            'hours_per_week': user_weights.hours_per_week_weight,
    # }
    if isinstance(user_weights, UserWeights):
        weights1 = { 'hours_per_week': user_weights.hours_per_week_weight }
    else:
        weights1 = { 'hours_per_week': user_weights['hours_per_week_weight'] }
    
    similarities = []
    for i, other_user in enumerate(all_users):
        euclidean_score = euclidean_similarity(
            {'hours_per_week': target_user.hours_per_week},
            {'hours_per_week': other_user.hours_per_week},
            weights1
        )
        jaccard_purpose = jaccard_similarity({target_user.purpose}, 
                                          {other_user.purpose})
        
        jaccard_self_assessment_lvl = jaccard_similarity({target_user.self_assessment_lvl}, 
                                          {other_user.self_assessment_lvl})
        
        jaccard_comm = jaccard_similarity({target_user.preferred_communication}, 
                                          {other_user.preferred_communication})
        
        if cosine_sim_games != 0:
            tfidf_games = cosine_sim_games[i]  # Сходство по играм
        else:
            tfidf_games = 0

        total_score = (0.2 * euclidean_score + 
                       0.2 * jaccard_purpose +
                       0.2 * jaccard_self_assessment_lvl +
                       0.1 * jaccard_comm +
                       0.3 * tfidf_games)  # Итоговый балл
        similarities.append((other_user.id, total_score))

    similarities.sort(key=lambda x: x[1], reverse=True)
    result = [(user_id[0], user_id[1]) for user_id in similarities[:top_n]]
    print(result)

    ret = {'info': 'ok'}
    if low_quality_flag:
        ret['info'] = 'low_quality'
    
    mates = []
    
    for i, u in enumerate(result):
        print(f'{i} - {u} - {u[0][0]} - {u[1]}')
        user = await UserDAO.get_by_id(u[0][0])
        mates.append({
            'user_id': user.id,
            'username': user.username,
            'score': u[1]
        })
        print(mates)
    
    ret.update({'mates': mates})
    
    await redis.redis.set(cache_key, json.dumps(ret), ex=1800)  # Кешируем на 30 минут
    
    return ret
