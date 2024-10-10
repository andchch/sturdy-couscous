from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.recommendation_system import find_best_matches
from api.models_sql import Base, User, UserProfile
from api.models_nosql import MongoDB, UserGames
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLAlchemy engine and session setup
# SQLALCHEMY_DATABASE_URL = 'postgresql://user:password@localhost/dbname'
SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///db.sqlite'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

MONGO_URI = 'mongodb://localhost:27017'
mongo_db = MongoDB(MONGO_URI)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создаем таблицы при старте
#@app.on_event('startup')
#def startup():
#    Base.metadata.create_all(bind=engine)

# Endpoint для получения информации о любимых играх пользователя (MongoDB)
@app.get('/user/{user_id}/games')
async def get_user_games(user_id: str):
    user_games = await mongo_db.get_user_games(user_id)
    return user_games

# Endpoint для добавления игр пользователя (MongoDB)
@app.post('/user/{user_id}/games')
async def add_user_games(user_id: str, games: UserGames):
    await mongo_db.add_user_games(games)
    return {'message': 'Games added'}

# Endpoint для создания нового пользователя (PostgreSQL)
@app.post('/users/')
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Endpoint для получения данных профиля пользователя (PostgreSQL)
@app.get('/users/{user_id}/profile')
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    return profile

# Endpoint для поиска игровых напарников
@app.get('/users/{user_id}/recommendations')
async def get_recommendations(user_id: int, db: Session = Depends(get_db)):
    matches = await find_best_matches(user_id, db)
    return {'recommended_users': matches}
