import re
class Calculator:
    def __init__(self, operation, a, b):
        if operation == '+':
            self.add(a, b)
        elif operation == '-':
            self.subtract(a, b)
        elif operation == '*':
            self.multiply(a, b)
        elif operation in('/', '\\'):
            self.divide(a, b)
        else:
            print('Я этого не умею.')

    def add(self, a, b):
        print(f'Сложение: {a} + {b} = {a + b}')

    def subtract(self, a, b):
        print(f'Вычитание: {a} - {b} = {a - b}')

    def multiply(self, a, b):
        print(f'Умножение: {a} * {b} = {a * b}')

    def divide(self, a, b):
        try:
            print(f'Деление: {a} / {b} = {a / b}')
        except ZeroDivisionError:
            print('Ошибка: деление на 0!')

try:
    operation, a, b = re.search(r'\.*(\d+)\s*(.)\s*(\d+)\.*', input('Введите выражение (в виде "2+2"): ').strip(' ')).group(2, 1, 3)
    Calculator(operation, int(a), int(b))
except:
    print('Неверный ввод')