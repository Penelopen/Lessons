def even_numbers(x):
    even_list = list(i for i in x if i % 2 == 0)

    if len(even_list) > 0:
        print('Четные числа:', even_list)
        sum_avg(even_list)
    else:
        print('Четные числа отсутствуют')

def sum_avg(x):
    print('Сумма четных чисел:', sum(x))
    print('Среднее значение четных чисел:', sum(x) / len(x))

even_numbers(list(map(int, input('Введите числа через пробел: ').split())))