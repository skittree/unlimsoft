import requests
from typing import Union
from config import WEATHER_API_KEY

class GetWeatherRequest():
    """
    Выполняет запрос на получение текущей погоды для города
    """

    def __init__(self):
        self.session = requests.Session()

    def get_weather(self, city) -> Union[float, None]:
        """
        Делает запрос на получение погоды. Возвращает температуру, если город существует.
        """
        url = 'https://api.openweathermap.org/data/2.5/weather?units=metric&q=' + city + '&appid=' + WEATHER_API_KEY
        r = self.session.get(url)
        if r.status_code == 200:
            weather = r.json()['main']['temp']
            return weather
        else:
            return None
        # can add a raise exception here for non 404 responses. do i need to?