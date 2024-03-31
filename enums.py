from enum import Enum


class Urls(Enum):
    COORDINATES_BY_LOCATION = 'http://api.openweathermap.org/geo/1.0/direct'
    CURRENT_WEATHER = 'https://api.openweathermap.org/data/2.5/weather'


class Units(Enum):
    STANDARD = 'standard'
    METRIC = 'metric'
    IMPERIAL = 'imperial'


class Language(Enum):
    RUSSIAN = 'ru'
    ENGLISH = 'en'
