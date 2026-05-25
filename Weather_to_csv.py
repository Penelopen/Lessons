import requests, sys, time, datetime
from config.global_config import weather_cfg

url = 'https://api.openweathermap.org/data/2.5/weather'
cities = ['Берлин', 'Пекин', 'Вашингтон', 'Манила', 'Бостон', 'Нью-Йорк', 'Пномпень', 'Бангкок', 'Анталья', 'Париж', 'Рим', 'Гуанчжоу', 'Венеция', 'Бали']

for new_file in range(120):
    try:
        now_datetime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        result = ''
        for city in cities:
            params = weather_cfg(city)
            res = requests.get(url, params).json()
            result += f"{now_datetime},{city},{res['main']['temp']},C\n"

        with open('log/weather.csv', 'w', encoding='UTF8') as file:
            file.write(result)
        print('DEBUG:', result)
    except Exception as e:
        print('DEBUG:', e)
        print('DEBUG:', res)
        sys.exit()
    time.sleep(60)