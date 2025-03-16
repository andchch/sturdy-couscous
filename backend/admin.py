from sqladmin import Admin, ModelView

from backend.main import app
from backend.core.database_sql import async_engine

from backend.api_v1.users.models_sql import Genre, User, UserContacts, UserFollow, UserInfo, UserWeights
from backend.api_v1.external_integration.models_sql import SteamProfile


admin = Admin(app, async_engine)

class UserAdmin(ModelView, model=User):
    column_list = [User.username, User.email]
    
class SteamProfileAdmin(ModelView, model=SteamProfile):
    column_list = [SteamProfile.user_id, SteamProfile.steam_id, SteamProfile.steam_name]
    
class GenreAdmin(ModelView, model=Genre):
    column_list = [Genre.id, Genre.name]
    
class UserFollowAdmin(ModelView, model=UserFollow):
    column_list = [UserFollow.follower_id, UserFollow.followed_id]
    
class UserContactsAdmin(ModelView, model=UserContacts):
    column_list = [UserContacts.id, UserContacts.user_id]
    
class UserWeightsAdmin(ModelView, model=UserWeights):
    column_list = [UserWeights.user_id]
    
class UserInfoAdmin(ModelView, model=UserInfo):
    column_list = [UserInfo.user_id]
    
admin.add_view(UserAdmin)
admin.add_view(SteamProfileAdmin)
admin.add_view(GenreAdmin)
admin.add_view(UserFollowAdmin)
admin.add_view(UserContactsAdmin)
admin.add_view(UserWeightsAdmin)
admin.add_view(UserInfoAdmin)
