import requests, pandas, sys
from config import params

url = 'https://api.currencylayer.com/timeframe'
params = params()

result = []
res = requests.get(url, params).json()

try:
    for val, item in res['quotes'].items():
        result.append([f"{val}", f"USD-RUB: {item['USDRUB']}", f"USD-EUR: {item['USDEUR']}"])
except:
    print(res)
    sys.exit()

result = pandas.DataFrame(result)
result.columns = ['Дата', 'Валютная пара', 'Курс к доллару']
print(result)
result.to_csv('currency.csv', index=False)
