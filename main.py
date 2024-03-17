
from typing import Optional

from fastapi import Depends, FastAPI, Response
from pydantic import BaseModel, Field

from enums import Language, Units
from weather import (City, Clouds, Coordinates, Main, Sys, Weather, Wind,
                     get_current_weather, get_location_by_name)

app = FastAPI()


class WeatherRequest(BaseModel):
    city: Optional[City] = Field('Москва', min_length=2)


class WeatherResponse(BaseModel):
    coord: Coordinates
    weather: list[Weather]
    visibility: int = Field(None, description='Visibility, meter')
    base: str = Field(None, description='Internal parameter')
    main: Main
    wind: Wind
    clouds: Clouds
    dt: int = Field(None, description='Time of data calculation, unix, UTC')
    sys: Sys
    timezone: int = Field(None, description='Shift in seconds from UTC')
    id: int = Field(None, description='City ID')
    name: str = Field(None, description='City name')
    cod: int = Field(None, description='Internal parameter')


class WeatherResponse404(BaseModel):
    city: City | None
    msg: str = 'локация города не определена'


@app.get("/weather/")
def get_weather_by_city(
        response: Response,
        city: WeatherRequest = Depends()
        ) -> WeatherResponse | WeatherResponse404:
    location = get_location_by_name(name=city.city)
    if not location:
        response.status_code = 404
        return WeatherResponse404(city=city.city)
    weather = get_current_weather(
        location=location, lang=Language.RUSSIAN, units=Units.METRIC)
    return WeatherResponse.model_validate(weather)
