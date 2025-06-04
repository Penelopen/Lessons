purchases = []
with open('purchases.csv') as input, open('Report.txt', 'w') as output:

    input.readline() ##пропускаем первую строку
    while True:
        line = input.readline().strip(' ').strip(']').strip(',\n') ##Причёсываем остальные
        if line == '':
            break
        purchases.append(eval(line)) ##Преобразуем строку в словарь


def total_revenue(purchases): ##Общая выручка (цена * количество для всех записей)
    total = 0
    for d in (purchases):
        total += d.get('price') * d.get('quantity')

    return f'Общая выручка: {total}'


def items_by_category(purchases): ##Словарь, где ключ — категория, а значение — список уникальных товаров в этой категории
    new_superspecial_dicto = {}
    for d in (purchases):
        try:
            new_superspecial_dicto[d.get('category')].append(d.get('item'))
        except KeyError:
            new_superspecial_dicto[d.get('category')] = [d.get('item')]

    return f'Товары по категориям: {new_superspecial_dicto}'


def expensive_purchases(purchases, min_price): ##Все покупки, где цена товара больше или равна min_price
    magic_list = []
    for d in (purchases):
        if d.get('price') >= min_price:
            magic_list.append(d)

    return f'Покупки дороже {min_price}: {', '.join(map(str, magic_list))}'


def average_price_by_category(purchases): ##Средняя цена товаров по каждой категории
    new_superspecial_dicto = {}
    for d in (purchases):
        try:
            new_superspecial_dicto[d.get('category')].append(d.get('price') * d.get('quantity'))
        except KeyError:
            new_superspecial_dicto[d.get('category')] = [d.get('price') * d.get('quantity')]

    for key, value in (new_superspecial_dicto.items()):
        new_superspecial_dicto[key] = [sum(value) / len(value)]

    return f'Средняя цена по категориям: {new_superspecial_dicto}'


def most_frequent_category(purchases): ##Категория, в которой куплено больше всего единиц товаров (с учётом поля quantity)
    new_superspecial_dicto = {}
    for d in (purchases):
        try:
            new_superspecial_dicto[d.get('category')] += (d.get('quantity'))
        except KeyError:
            new_superspecial_dicto[d.get('category')] = (d.get('quantity'))

    return f'Категория с наибольшим количеством проданных товаров: {sorted(new_superspecial_dicto, key=lambda x: (x[1]))[-1]}'


print(total_revenue(purchases))
print(items_by_category(purchases))
print(expensive_purchases(purchases, 1.0))
print(average_price_by_category(purchases))
print(most_frequent_category(purchases))
