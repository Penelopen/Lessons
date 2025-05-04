import yaml, json, pandas
class MyClass:
    data = ''
    def data_info(self):
        print(self.data)

    def yaml_read(file, self):
        with open(file) as yaml_in:
            self.data = yaml.load(yaml_in, Loader=yaml.FullLoader)

    def yaml_save(file, self):
        with open(file, 'w') as yaml_out:
            yaml.dump(self.data, yaml_out)
            yaml_out.write(str(self.data))

    def json_read(file, self):
        with open(file) as json_in:
            self.data = json.dumps(json.load(json_in), indent=4)

    def json_save(file, self):
        with open(file, 'w') as json_out:
            json.dump(self.data, json_out)
            json_out.write(str(self.data))

    def csv_read(file, self):
        self.data = pandas.read_csv(file)

    def csv_save(file, self):
        pandas.DataFrame(self.data).to_csv(file, index=False)

my_file = MyClass()
MyClass.csv_read('test.csv', my_file)
MyClass.data_info(my_file)