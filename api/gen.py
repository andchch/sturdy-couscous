from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models_sql import User, UserProfile, PreferredGenre, UserPlatform
from models_nosql import MongoDB

fake = Faker()
MONGO_URI = 'mongodb://localhost:27017'
mongo_db = MongoDB(MONGO_URI)

GENRES = ['Action', 'Adventure', 'RPG', 'FPS', 'MOBA', 'Strategy', 'Sports', 'MMO', 'Puzzle']
PLATFORMS = ['PC', 'PS5', 'Xbox', 'Nintendo Switch', 'Mobile']
LEVELS = ['Beginner', 'Intermediate', 'Advanced']
MOTIVATIONS = ['For fun', 'For competition']

def generate_user_data(db: Session):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    gender = random.choice(['Male', 'Female', 'Other'])
    age = random.randint(18, 45)
    language = random.choice(['English', 'Russian', 'Spanish', 'German', 'Chinese'])
    timezone = fake.timezone()

    user = User(username=username, email=email, password=password, gender=gender, age=age, language=language, timezone=timezone)
    db.add(user)
    db.commit()

    self_assessment_level = random.choice(LEVELS)
    motivation = random.choice(MOTIVATIONS)
    preferred_time_of_day = random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])
    playtime_per_week = random.randint(5, 30)
    preferred_days = random.sample(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 3)
    
    user_profile = UserProfile(user_id=user.id, self_assessment_level=self_assessment_level, motivation=motivation, 
                               preferred_time_of_day=preferred_time_of_day, playtime_per_week=playtime_per_week, 
                               preferred_days=','.join(preferred_days))
    db.add(user_profile)
    
    preferred_genres = random.sample(GENRES, 3)
    for genre in preferred_genres:
        db.add(PreferredGenre(user_id=user.id, genre=genre))
    
    preferred_platforms = random.sample(PLATFORMS, random.randint(1, 2))
    for platform in preferred_platforms:
        db.add(UserPlatform(user_id=user.id, platform=platform))
    
    db.commit()

    favorite_games = [{'game_name': f'Game {i+1}', 'rank': random.randint(1, 100), 'rating': random.uniform(1, 10), 'position': random.choice(['Attacker', 'Defender'])} for i in range(random.randint(3, 5))]
    
    mongo_db.insert_user_games(str(user.id), {'favorite_games': favorite_games})

def generate_test_data(n: int, db: Session):
    for _ in range(n):
        generate_user_data(db)
    print(f'Successfully generated {n} users with profiles, genres, platforms, and favorite games.')


if __name__ == '__main__':
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite'
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    generate_test_data(1, db)
