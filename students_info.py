## Вводные данные:
students = [
    {"name": "Иван", "age": 20, "grades": {"математика": 4, "физика": 5, "химия": 3}},
    {"name": "Мария", "age": 19, "grades": {"математика": 5, "физика": 5, "химия": 5}},
    {"name": "Пётр", "age": 21, "grades": {"математика": 3, "физика": 4, "химия": 2}},
    {"name": "Анна", "age": 22, "grades": {"математика": 5, "физика": 4, "химия": 4}},
    {"name": "Александр", "age": 19, "grades": {"математика": 3, "физика": 3, "химия": 3}}
]

students_age = {}
students_avg = {}
sum_grade = {}
avg_grade = {}

for dic in students:
    ## Инвертированный словарь для вычисления самого младшего студента. С учётом нескольких студентов одного возраста
    if dic.get('age') in students_age:
        students_age[dic.get('age')].append(dic.get('name'))
    else:
        students_age[dic.get('age')] = [dic.get('name')]

    curr_student_sum = 0
    for subj, grade in dic.get('grades').items():
        curr_student_sum += grade
        if subj in sum_grade:
            sum_grade[subj] += grade
        else:
            sum_grade[subj] = grade

        ## Словарь для средних оценок по предметам
        avg_grade[subj] = round(sum_grade.get(subj) / len(students), 2)

    ## Словарь для средних оценок студентов
    students_avg[dic.get('name')] = round(curr_student_sum / len(dic.get('grades')), 2)

max_avg_student = next([key, value] for key, value in students_avg.items() if value == max(students_avg.values()))
max_average_subj = next([key, value] for key, value in avg_grade.items() if value == max(avg_grade.values()))

print(f'Самый младший студент: {' и '.join(students_age.get(min(students_age)))}, возраст: {min(students_age)}')
print(f'Студент с самой высокой средней оценкой: {max_avg_student[0]}, средний балл: {max_avg_student[1]}')
print(f'Предмет с самым высоким средним баллом: {max_average_subj[0]}, средний балл: {max_average_subj[1]}')
print('Студенты с баллом выше 3.0:')
for name, grade in students_avg.items():
    if grade > 3.0:
        print(f'{name}: средний балл = {grade}')

