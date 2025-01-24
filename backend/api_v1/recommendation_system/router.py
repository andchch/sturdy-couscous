from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.recommendation_system.rs import find_teammates
from backend.api_v1.recommendation_system.schemas import finderResponse
from backend.core.database_mongo import MongoController, get_mongo_controller
from backend.redis.cache import RedisController, get_redis_controller


rs_router = APIRouter(prefix='/rs', tags=['RS management'])


@rs_router.get('/{user_id}/find', response_model=finderResponse)
async def find_teammate(user_id: int, 
                        mongo: Annotated[MongoController, Depends(get_mongo_controller)], 
                        redis: Annotated[RedisController, Depends(get_redis_controller)]):
    ids = await find_teammates(user_id, mongo, redis)
    return ids
