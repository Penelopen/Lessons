import requests
from config import weather_cfg

city = str(input('Введите название города: '))
url = 'https://api.openweathermap.org/data/2.5/weather'
params = weather_cfg(city)

res = requests.get(url, params).json()
print(f"Температура в г.{city.title()}: {res['main']['temp']}, C")