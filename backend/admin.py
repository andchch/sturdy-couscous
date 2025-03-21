from sqladmin import Admin, ModelView

from backend.core.database_sql import async_engine

from backend.api_v1.users.models_sql import Genre, User, UserContact, UserFollow, UserInfo, UserWeight, user_genre_association_table
from backend.api_v1.external_integration.models_sql import SteamProfile


class UserAdmin(ModelView, model=User):
    column_list = [User.username, User.email]
    
class SteamProfileAdmin(ModelView, model=SteamProfile):
    column_list = [SteamProfile.user_id, SteamProfile.steam_id, SteamProfile.steam_name]
    
class GenreAdmin(ModelView, model=Genre):
    column_list = [Genre.id, Genre.name]
    
class UserFollowAdmin(ModelView, model=UserFollow):
    column_list = [UserFollow.follower_id, UserFollow.followed_id]
    
class UserContactAdmin(ModelView, model=UserContact):
    column_list = [UserContact.id, UserContact.user_id]
    
class UserWeightAdmin(ModelView, model=UserWeight):
    column_list = [UserWeight.user_id]
    
class UserInfoAdmin(ModelView, model=UserInfo):
    column_list = [UserInfo.user_id]

def create_admin(app):
    admin = Admin(app, async_engine)

    admin.add_view(UserAdmin)
    admin.add_view(SteamProfileAdmin)
    admin.add_view(GenreAdmin)
    admin.add_view(UserFollowAdmin)
    admin.add_view(UserContactAdmin)
    admin.add_view(UserWeightAdmin)
    admin.add_view(UserInfoAdmin)
