def file_rw(in_data, csv_columns, type_method, file_name):
    import yaml, json, pandas, sys
    from pathlib import Path
    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    class MyClass:
        data = in_data
        def data_info(self):
            print(self.data)

        def text_append(file_name, self):
            with open(file_name, 'a') as text_out:
                for string in self.data:
                    text_out.write('\n' + str(string))

        def yaml_read(file_name, self):
            with open(file_name) as yaml_in:
                self.data = yaml.load(yaml_in, Loader=yaml.FullLoader)

        def yaml_save(file_name, self):
            with open(file_name, 'w') as yaml_out:
##                yaml.dump(self.data, yaml_out)
                yaml_out.write(str(self.data) + '\n')

        def json_read(file_name, self):
            with open(file_name) as json_in:
                self.data = json.dumps(json.load(json_in), indent=4)

        def json_save(file_name, self):
            with open(file_name, 'w') as json_out:
##                json.dump(self.data, json_out)
                json_out.write(str(self.data) + '\n')

        def csv_read(file_name, self):
            self.data = pandas.read_csv(file_name)

        def csv_save(file_name, csv_columns, self):
            res = pandas.DataFrame(self.data)
            res.columns = csv_columns
            print(res)
            res.to_csv(file_name, encoding='windows-1251', index=True)

    my_file = MyClass()
    if type_method == 'text_append':
        MyClass.text_append(file_name, my_file)
        sys.exit()
    elif type_method == 'yaml_read':
        MyClass.yaml_read(file_name, my_file)
    elif type_method == 'yaml_save':
        MyClass.yaml_save(file_name, my_file)
    elif type_method == 'json_read':
        MyClass.json_read(file_name, my_file)
    elif type_method == 'json_save':
        MyClass.json_save(file_name, my_file)
    elif type_method == 'csv_read':
        MyClass.csv_read(file_name, my_file)
    elif type_method == 'csv_save':
        MyClass.csv_save(file_name, csv_columns, my_file)
        sys.exit()

    MyClass.data_info(my_file)

##file_rw(['1', '2', '3'], ['A', 'B', 'C'], 'csv_save', 'log/teeeeeeest.csv')