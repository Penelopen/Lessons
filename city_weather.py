import requests, sys, datetime
from config.global_config import weather_cfg
from json_yaml_csv_rw import file_rw

##cities = [str(input(f'Введите название города {i}(5): ')) for i in range(1, 6)]
cities = ['берлин', 'токио', 'Денвер', 'Пекин', 'брест']
url = 'https://api.openweathermap.org/data/2.5/weather'
result = []
result_columns = ['Время', 'Город', 'Температура']
now_datetime = datetime.datetime.now().strftime('%d-%m-%Y %H_%M_%S')

try:
    for city in cities:
        params = weather_cfg(city)
        res = requests.get(url, params).json()
        result.append([now_datetime, f"{city.title()}:", f"{res['main']['temp']} C"])
    file_rw(result, result_columns, 'csv_save', f'log/{now_datetime}.csv')
except Exception as e:
    print(e)
    print(res)
    sys.exit()