import json
import os
from dataclasses import dataclass
from typing import TypeAlias, TypedDict

import requests

from enums import Language, Units, Urls


OPEN_WEATHER_KEY = os.environ.get("OPEN_WEATHER_KEY")

if not OPEN_WEATHER_KEY:
    raise 'Не задан OPEN_WEATHER_KEY в переменных окружения'


Lat: TypeAlias = int
Lon: TypeAlias = int


@dataclass(slots=True, kw_only=True)
class Coordinates:
    lat: Lat
    lon: Lon


class LocationParams(TypedDict):
    appid: str | None
    q: str
    limit: int


class WeatherParams(TypedDict):
    appid: str | None
    lang: str
    units: str
    lat: Lat
    lon: Lon


def get_json_data(url: str, params: LocationParams | WeatherParams) -> dict:
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def get_location_by_name(name: str) -> Coordinates | None:
    location = get_json_data(url=Urls.COORDINATES_BY_LOCATION.value, params={
        'appid': OPEN_WEATHER_KEY,
        'limit': 1,
        'q': name,
    })
    if not location:
        return None
    return Coordinates(lat=location[0]['lat'], lon=location[0]['lon'])


def get_current_weather(
        location: Coordinates, lang: Language, units: Units) -> dict:
    return get_json_data(url=Urls.CURRENT_WEATHER.value, params={
        'appid': OPEN_WEATHER_KEY,
        'lat': location.lat,
        'lon': location.lon,
        'lang': lang.value,
        'units': units.value,
    })
