import requests, pandas, sys
from config import currency_cfg

url = 'https://api.currencylayer.com/timeframe'
params = currency_cfg()

result = []

try:
    res = requests.get(url, params).json()
    for val, item in res['quotes'].items():
        result.append([val, f'{list(item)[0]}: {list(item.values())[0]}', f'{list(item)[1]}: {list(item.values())[1]}'])
except Exception as e:
    print(e)
    print(res)
    sys.exit()

result = pandas.DataFrame(result)
result.columns = ['Дата', 'Валюта 1', ' Валюта 2']
print(result)
result.to_csv('currency.csv', index=False)