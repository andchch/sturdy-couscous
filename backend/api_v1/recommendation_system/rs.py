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

def calculate_genre_similarity(user1_genres, user2_genres):
    mlb = MultiLabelBinarizer()
    genres_encoded = mlb.fit_transform([user1_genres, user2_genres])
    return cosine_similarity(genres_encoded)[0, 1]


# def calculate_playtime_similarity(user1_playtime, user2_playtime):
#     user1_times = np.array(list(user1_playtime.values()))
#     user2_times = np.array(list(user2_playtime.values()))
#     return cosine_similarity([user1_times], [user2_times])[0, 0]


# def calculate_day_similarity(user1_days, user2_days):
#     mlb = MultiLabelBinarizer()
#     days_encoded = mlb.fit_transform([user1_days, user2_days])
#     return cosine_similarity(days_encoded)[0, 1]


def calculate_total_similarity(user1: UserProfile, user2: UserProfile):    
    purpose_weight = 0.2
    self_assessment_lvl_weight = 0.2
    preferred_communication_weight = 0.2
    preferred_platforms_weight = 0.2
    playtime_weight = 0.2
    hours_per_week_weight = 0.2
    preferred_days_weight = 0.2
    preferred_genres_weight = 0.2

    # genre_similarity = calculate_genre_similarity(user1.preferred_genres, user2.preferred_genres)
    # playtime_similarity = calculate_playtime_similarity(user1.playtime, user2.playtime)
    # day_similarity = calculate_day_similarity(user1.preferred_days, user2.preferred_days)
    self_ass_lvl_similarity = 1 if user1.self_ass_lvl == user2.self_ass_lvl else 0
    # genre_similarity = calculate_genre_similarity(user1.platforms, user2.platforms)
    platform_similarity = calculate_genre_similarity(user1.platforms, user2.platforms)
    purpose_similarity = 1 if user1.purpose == user2.purpose else 0

    total_similarity = (
        # preferred_genres_weight * genre_similarity +
        # playtime_weight * playtime_similarity +
        # days_weight * day_similarity +
        self_assessment_lvl_weight * self_ass_lvl_similarity +
        preferred_platforms_weight * platform_similarity +
        purpose_weight * purpose_similarity
    )
    
    return total_similarity


def find_similar_users(current_user: UserProfile, users: List[UserProfile], top_n=3):
    similarities = []
    
    for user in users:
        if user.user_id != current_user.user_id:
            similarity = calculate_total_similarity(current_user, user)
            similarities.append((user.user_id, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_n]

# start_time = time.time()
# similar_users = find_similar_users(users2[0], users2)
# end_time = time.time()
# print(f'Similar users to user 1: {similar_users}')
# print(f'Time spent: {end_time - start_time}')
