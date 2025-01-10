from pydantic import BaseModel

class Game(BaseModel):
    appid: int
    name: str
    playtime_forever: int
    img_icon_url: str
    # has_community_visible_stats: bool | None
    playtime_windows_forever: int
    playtime_mac_forever: int
    playtime_linux_forever: int
    playtime_deck_forever: int
    rtime_last_played: int
    # content_descriptorids: list[int] | None
    playtime_disconnected: int
    
class GetGames(BaseModel):
    game_count: int
    games: list[Game]
    
class GetGamesResponse(BaseModel):
    steam_id: str
    response: GetGames
    
class Friend(BaseModel):
    steamid: str
    relationship: str
    friend_since: int
    
class Friendlist(BaseModel):
    friends: list[Friend]
    
class GetFriendsResponse(BaseModel):
    friendslist: Friendlist | str
    