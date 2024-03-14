from typing import Union

from fastapi import FastAPI, Response

from enums import Language, Units
from weather import get_current_weather, get_location_by_name


app = FastAPI()


@app.get("/weather/")
def read_item(response: Response, city: Union[str, None] = None) -> dict:
    if not city:
        response.status_code = 400
        return {"msg": "не указан город"}
    location = get_location_by_name(name=city)
    if not location:
        response.status_code = 404
        return {"city": city, "msg": "локация города не определена"}
    weather = get_current_weather(
        location=location, lang=Language.RUSSIAN, units=Units.METRIC)
    return {"city": city, "location": location, "weather": weather}
