# Получение данных пользователя и их сохранение
from fastapi import APIRouter, requests

from backend.api_v1.games.dao import GameDAO
from backend.api_v1.games.models_sql import Achievement, Game
from backend.api_v1.users.dao import AchievementDAO
from backend.core.config import get_steam_api_key


ext_integration_router = APIRouter(prefix='/ext', tags=['External integration'])


@ext_integration_router.get('/fetch-data')
async def fetch_data(steamid: str):
    owned_games = fetch_owned_games(get_steam_api_key(), steamid)

    # Сохранение игр
    for game in owned_games:
        db_game = GameDAO.get_by_app_steam_id(game['appid'], steamid)
        if not db_game:
            db_game = Game(
                steamid=steamid,
                appid=game['appid'],
                name=game['name'],
                playtime_hours=game['playtime_forever'] / 60,
            )
            GameDAO.create(db_game)

    # Сохранение достижений
    for game in owned_games:
        appid = game['appid']
        game_achievements = fetch_achievements(get_steam_api_key(), steamid, appid)
        for achievement in game_achievements:
            db_achievement = AchievementDAO.get_by_app_steam_id(
                appid, steamid, achievement['name']
            )

            if not db_achievement:
                db_achievement = Achievement(
                    steamid=steamid,
                    appid=appid,
                    achievement=achievement['name'],
                    unlocked=achievement['unlocked'],
                )
                AchievementDAO.create(db_achievement)

    return {'message': 'Data fetched and saved'}


# Функции работы с API Steam
def fetch_user_summary(api_key, steamid):
    url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'
    params = {'key': api_key, 'steamids': steamid}
    response = requests.get(url, params=params).json()
    return response['response']['players'][0]


def fetch_owned_games(api_key, steamid):
    url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
    params = {'key': api_key, 'steamid': steamid, 'include_appinfo': True}
    response = requests.get(url, params=params).json()
    return response['response']['games']


def fetch_achievements(api_key, steamid, appid):
    url = 'https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/'
    params = {'key': api_key, 'steamid': steamid, 'appid': appid}
    response = requests.get(url, params=params).json()
    return response['playerstats']['achievements']