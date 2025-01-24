from backend.api_v1.users.dao import UserDAO


class Weights():
    purpose_weight: int
    self_assessment_lvl_weight: int
    preferred_communication_weight: int
    preferred_platforms_weight: int
    
    playtime_weight: int
    hours_per_week_weight: int
    preferred_days_weight: int
    preferred_genres_weight: int


class UserRSProfile():
    def __init__(self, id, purpose, 
                 self_assessment_lvl, 
                 preferred_communication, 
                 hours_per_week):
        self.id=id,
        self.purpose=purpose
        self.self_assessment_lvl=self_assessment_lvl
        self.preferred_communication=preferred_communication
        self.hours_per_week=hours_per_week
    
    
class UserRSProfileDAO():
    @classmethod
    async def get_rs_profile_by_id(cls, user_id: int) -> UserRSProfile | None:
        user = await UserDAO.get_by_id_with_rs_info(user_id)
        if not user:
            return None
        else:
            if not user.info:
                return None
            else:
                return UserRSProfile(user.id,
                                    user.info.purpose,
                                    user.info.self_assessment_lvl,
                                    user.info.preferred_communication,
                                    user.info.hours_per_week)
    
    @classmethod
    async def get_all_others(cls, user_id: int) -> list[UserRSProfile]:
        users = await UserDAO.get_others(user_id)
        if not users:
            return None
        else:
            ret = []
            for ui in users:
                if not ui.info:
                    pass
                else:
                    ret.append(UserRSProfile(ui.id, ui.info.purpose,
                                  ui.info.self_assessment_lvl,
                                  ui.info.preferred_communication,
                                  ui.info.hours_per_week))
        return ret