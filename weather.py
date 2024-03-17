import json
import os
from dataclasses import dataclass
from typing import TypeAlias, TypedDict

import requests
from pydantic import Field

from enums import Language, Units, Urls


OPEN_WEATHER_KEY = os.environ.get("OPEN_WEATHER_KEY")

if not OPEN_WEATHER_KEY:
    raise 'Не задан OPEN_WEATHER_KEY в переменных окружения'


City: TypeAlias = str
Lat: TypeAlias = float
Lon: TypeAlias = float


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


@dataclass
class Weather:
    id: int = Field(None, description='Weather condition id')
    main: str = Field(None, description='Group of weather parameters (Rain, Snow, Clouds etc.)')  # noqa: E501
    description: str = Field(None, description='Weather condition within the group')  # noqa: E501
    icon: str = Field(None, description='Weather icon id')


@dataclass
class Main:
    temp: float = Field(None, description='Temperature')
    feels_like: float = Field(None, description='Temperature. This temperature parameter accounts for the human perception of weather')  # noqa: E501
    temp_min: float = Field(None, description='Minimum temperature at the moment')  # noqa: E501
    temp_max: float = Field(None, description='Maximum temperature at the moment')  # noqa: E501
    pressure: int = Field(None, description='Atmospheric pressure on the sea level, hPa')  # noqa: E501
    humidity: int = Field(None, description='Humidity, %')
    sea_level: int = Field(None, description='Atmospheric pressure on the sea level, hPa')  # noqa: E501
    grnd_level: int = Field(None, description='Atmospheric pressure on the ground level, hPa')  # noqa: E501


@dataclass
class Wind:
    speed: float = Field(None, description='Wind speed')
    deg: int = Field(None, description='Wind direction, degrees')
    gust: float = Field(None, description='Wind gust')


@dataclass
class Clouds:
    all: int = Field(None, description='Cloudiness, %')


@dataclass
class Sys:
    type: int = Field(None, description='Internal parameter')
    id: int = Field(None, description='Internal parameter')
    country: str = Field(None, description='Country code (GB, JP etc.)')
    sunrise: int = Field(None, description='Sunrise time, unix, UTC')
    sunset: int = Field(None, description='Sunset time, unix, UTC')


@dataclass
class Coordinates:
    lon: Lon = Field(None, description='Longitude of the location')
    lat: Lat = Field(None, description='Latitude of the location')


def get_json_data(url: str, params: LocationParams | WeatherParams) -> dict:
    response = requests.get(url=url, params=params)
    return json.loads(response.text)


def get_location_by_name(name: str | None) -> Coordinates | None:
    if not name:
        return None
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
