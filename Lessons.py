##import yaml, json, pandas
##class MyClass:
##    connections = ''
##    data = ''
##    def yaml_info(self):
##        print(self.connections)
##
##    def yaml_read(file, self):
##        with open(file) as yaml_in:
##            self.connections = yaml.load(yaml_in, Loader=yaml.FullLoader)
##
##    def yaml_save(file, self):
##        with open(file, 'w') as yaml_out:
##            yaml.dump(self.connections, yaml_out)
####            yaml_out.write(str(self.connections))
##
##    def json_info(self):
##        print(self.connections)
##
##    def json_read(file, self):
##        with open(file) as json_in:
##            self.connections = json.dumps(json.load(json_in), indent=4)
##
##    def json_save(file, self):
##        with open(file, 'w') as json_out:
##            json.dump(self.connections, json_out)
####            json_out.write(str(self.connections))
##
##    def csv_info(self):
##        print(self.data)
##
##    def csv_read(file, self):
##        self.data = pandas.read_csv(file)
##
##    def csv_save(file, self):
##        pandas.DataFrame(self.data).to_csv(file, index=False)
##
##my_file = MyClass()
##MyClass.yaml_read('sex1.yaml', my_file)
##MyClass.json_info(my_file)

import requests, pandas
url = 'https://api.currencylayer.com/timeframe'
params = {
    'access_key': '1bbd0e4feae573037172783bf5a5ac2b',
    'currencies': 'RUB,EUR',
    'start_date': '2023-11-01',
    'end_date': '2023-11-30'
}
result = []
res = requests.get(url, params)
print(res.json())
print(res.status_code)
##for val, item in res['quotes'].items():
##    result.append([f"{val}", f"USD-RUB: {item['USDRUB']}", f"USD-EUR: {item['USDEUR']}"])
##
##result = pandas.DataFrame(result)
##result.columns = ['Дата', 'Валютная пара', 'Курс к доллару']
##print(result)
##result.to_csv('sex.csv', index=False)
