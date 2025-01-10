import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_DB: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    
    S3_TENANT_ID: str
    S3_KEY_ID: str
    S3_KEY_SECRET: str
    S3_ENDPOINT: str
    
    JWT_EXPIRATION_DAYS: int
    SECRET_KEY: str
    ALGORITHM: str
    
    STEAM_API_KEY: str
    
    REDIS_URI: str
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', '..' ,'.env'
        )
    )


settings = Settings()


def get_db_uri() -> str:
    return (
        f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@'
        f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    )
    
def get_mongo_uri() -> str:
    return (
        f'mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@'
        f'{settings.MONGO_HOST}:{settings.MONGO_PORT}'
    )
    
def get_mongo_db() -> str:
    return settings.MONGO_DB


def get_auth_data() -> dict:
    return {'secret_key': settings.SECRET_KEY, 'algorithm': settings.ALGORITHM}


def get_jwt_expiration():
    return settings.JWT_EXPIRATION_DAYS

def get_steam_api_key():
    return settings.STEAM_API_KEY

def get_s3_creds():
    return [settings.S3_TENANT_ID, settings.S3_KEY_ID,
            settings.S3_KEY_SECRET, settings.S3_ENDPOINT]

def get_redis_db():
    return settings.REDIS_URI
