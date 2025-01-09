from typing import Annotated
from fastapi import APIRouter, Depends

from backend.api_v1.communities.dao import CommunityDAO, CommunityMembershipDAO
from backend.api_v1.communities.models_sql import Community
from backend.api_v1.communities.schemes import CommunityCreate, CommunityCreateResponse, CommunityJoinResponse, CommunityListResponse, EditCommunity
from backend.api_v1.communities.utilities import serialize_community_with_members, serialize_full_community
from backend.api_v1.users.dependencies import get_current_user
from backend.api_v1.users.models_sql import User

from .exceptions import community_exists, community_not_found, already_joined


community_router = APIRouter(prefix='/community', tags=['Communities management'])


@community_router.post("/create", response_model=CommunityCreateResponse)
async def create_community(data: CommunityCreate, current_user: Annotated[User, Depends(get_current_user)]):
    data = data.model_dump()
    # Проверяем, существует ли уже сообщество с таким именем
    existing_community = await CommunityDAO.get_by_name(data['name'])
    if existing_community:
        raise community_exists
    # Создаем новое сообщество
    new_community = await CommunityDAO.create(
        name=data['name'],
        description=data['description'],
        creator_id=current_user.id
    )
    return {"id": new_community.id, "name": new_community.name}


@community_router.post("/{community_id}/join", response_model=CommunityJoinResponse)
async def join_community(community_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    # Проверяем, существует ли сообщество
    community = await CommunityDAO.get_by_id(community_id)
    if not community:
        raise community_not_found

    # Проверяем, является ли пользователь уже участником
    existing_membership = await CommunityMembershipDAO.get_user_membership(user_id=current_user.id,
                                                                     community_id=community_id)
    if existing_membership:
        raise already_joined

    # Добавляем участника
    membership = await CommunityMembershipDAO.create(user_id=current_user.id,
                                                     community_id=community_id,
                                                     role="member")

    return {"message": f"User {current_user.id} joined community {community.name}"}


@community_router.patch('/{community_id}/edit')
async def edit_community(community_id: int, new_data: EditCommunity):
    await CommunityDAO.update(community_id, **new_data.model_dump())
    return {'status': 'haghaga'}
    

@community_router.get("/", response_model=list[CommunityListResponse])
async def list_communities(skip: int = 0, limit: int = 10):
    communities = await CommunityDAO.get_all(skip, limit)
    return [serialize_community_with_members(community) for community in communities]

@community_router.get('/{community_id}')
async def get_community(community_id: int, skip: int = 0, limit: int = 10):
    community = await CommunityDAO.get(community_id, skip, limit)
    return serialize_full_community(community)
