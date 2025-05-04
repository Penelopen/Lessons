def currency_cfg():
    return {
    'access_key': '6f3df93ed33afa4a70563cccea086f93',
    'currencies': 'RUB,EUR',
    'start_date': '2023-11-01',
    'end_date': '2023-11-30'
    }


def weather_cfg(city):
    return {
    'appid': '11c0d3dc6093f7442898ee49d2430d20',
    'q': city,
    'units': 'metric'
    }