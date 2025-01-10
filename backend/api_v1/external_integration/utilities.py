from datetime import datetime
import httpx
import json

from backend.core.config import get_steam_api_key

STEAM_BASE_URL = 'https://api.steampowered.com'


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


async def fetch_steam_data(endpoint: str, params: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{STEAM_BASE_URL}/{endpoint}', params={'key': get_steam_api_key(), **params})
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError:
            return {'error': 'privacy'}

        return response.json()
    
async def fetch_steam_profile(steam_id: str):
    resp = await fetch_steam_data('ISteamUser/GetPlayerSummaries/v2/', {'steamids': steam_id})
    data = {}
    if 'response' in resp and 'players' in resp['response']:
        player = resp['response']['players'][0]
        
        data['steam_id'] = player.get('steamid')
        data['steam_name'] = player.get('personaname')
        data['steam_avatar'] = player.get('avatar')
        data['profile_url'] = player.get('profileurl')
    return data

async def fetch_owned_games(steam_id: str):
    data = await fetch_steam_data('IPlayerService/GetOwnedGames/v1/', {'steamid': steam_id, 'include_appinfo': True})
    return data

async def fetch_achievements(steam_id: str, app_id: str):
    data = await fetch_steam_data('ISteamUserStats/GetPlayerAchievements/v1/', {'steamid': steam_id, 'appid': app_id})
    return data

async def fetch_friends(steam_id: str):
    data = await fetch_steam_data('ISteamUser/GetFriendList/v1/', {'steamid': steam_id, 'relationship': 'friend'})
    return data
