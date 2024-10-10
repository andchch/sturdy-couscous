from sqlalchemy.orm import Session
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

from api.models_sql import User, UserProfile, PreferredGenre
from api.models_nosql import MongoDB

MONGO_URI = 'mongodb://localhost:27017'
mongo_db = MongoDB(MONGO_URI)

async def get_user_data(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    genres = db.query(PreferredGenre).filter(PreferredGenre.user_id == user_id).all()
    genres = [genre.genre for genre in genres]

    games = await mongo_db.get_user_games(str(user_id))
    favorite_games = [game['game_name'] for game in games['favorite_games']]

    return {
        'user': user,
        'profile': profile,
        'genres': genres,
        'favorite_games': favorite_games
    }


def compute_similarity(user_data_1, user_data_2):
    mlb = MultiLabelBinarizer()
    genre_matrix = mlb.fit_transform([user_data_1['genres'], user_data_2['genres']])
    genre_similarity = cosine_similarity(genre_matrix)[0][1]
    
    game_matrix = mlb.fit_transform([user_data_1['favorite_games'], user_data_2['favorite_games']])
    game_similarity = cosine_similarity(game_matrix)[0][1]
    
    level_similarity = 1 if user_data_1['profile'].self_assessment_level == user_data_2['profile'].self_assessment_level else 0
    
    motivation_similarity = 1 if user_data_1['profile'].motivation == user_data_2['profile'].motivation else 0
    
    total_similarity = (0.4 * genre_similarity + 
                        0.4 * game_similarity + 
                        0.1 * level_similarity + 
                        0.1 * motivation_similarity)
    
    return total_similarity


async def find_best_matches(user_id: int, db: Session, top_n: int = 5):
    current_user_data = await get_user_data(user_id, db)
    other_users = db.query(User).filter(User.id != user_id).all()

    matches = []
    for other_user in other_users:
        other_user_data = await get_user_data(other_user.id, db)
        similarity = compute_similarity(current_user_data, other_user_data)
        
        matches.append({
            'user_id': other_user.id,
            'username': other_user.username,
            'similarity': similarity
        })

    matches.sort(key=lambda x: x['similarity'], reverse=True)
    
    return matches[:top_n]
