import requests
from datetime import datetime
from datetime import timezone
from config_data.config import Config, load_config
from database.database import users_db


config: Config = load_config()

#Get the id of the track
def create_track_and_get_id(track: str):
    url = "https://postal-ninja.p.rapidapi.com/v1/track"

    payload = { "trackCode": track }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept": "application/json; charset=UTF-8",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": config.tg_bot.rapid_api_key,
        "X-RapidAPI-Host": "postal-ninja.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()['pkgId']



def get_response(track_id):
    url = f"https://postal-ninja.p.rapidapi.com/v1/track/{track_id}"

    querystring = {"await":"false","lang":"RU"}

    headers = {
        "Accept": "application/json; charset=UTF-8",
        "X-RapidAPI-Key": config.tg_bot.rapid_api_key,
        "X-RapidAPI-Host": "postal-ninja.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response


#Get the information about the track
def get_track_info_list(track_id: int):

    response = get_response(track_id)

    track_list = []

    for event in response.json()['pkg']['events']:
        d = datetime.fromisoformat(event['dt']).astimezone(timezone.utc)
        track_list.append(d.strftime('%Y-%m-%d %H:%M:%S') + '-' +  event['dsc'])

    return ('\n').join(track_list)


def get_last_track_info(track_id: int):

    track_list = []

    response = get_response(track_id)


    for event in response.json()['pkg']['events']:
        d = datetime.fromisoformat(event['dt']).astimezone(timezone.utc)
        track_list.append(d.strftime('%Y-%m-%d %H:%M:%S') + '-' +  event['dsc'])

    return track_list[-1]

    
        