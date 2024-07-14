import os
import types

def logger(path):
    import datetime

    def __logger(old_function):
        def new_function(*args, **kwargs):
            current_datetime = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            print(f'''
            Функция {old_function.__name__} была вызвана в {current_datetime}
            с аргументами {args} и {kwargs}
            и вернула аргумент {result}
            ''')
            input_str = str(current_datetime) + " " + str(old_function.__name__) + " " + str(args) + " " + str(
                kwargs) + " " + str(result) + "\n"
            with open(path, 'a') as fp:
                fp.write(input_str)
            return result
        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

class Student:
    path = "log_4.log"

    @logger(path)
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    @logger(path)
    def rate_lector(self, lector, course, grade):
        if isinstance(course, str) and (course in self.courses_in_progress):
            if isinstance(grade, int) and (0 <= grade <= 10):
                # Как сопоставить лектора и студента?
                #Нужно организовать проверку на совпадение курса у лектора и студента?
                # Или просто вводим класс лектора на входе вместо его имени?<-пока делаю так
                # Тогда просто нужно проверить, есть ли общий course у студента и у лектора.
                if isinstance(lector, Lecturer) and (course in lector.courses_attached):
                    lector.ratings[course] = grade


class Mentor:

    path = "log_4.log"

    @logger(path)
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        # Получается что у нас может быть только 1 курс на ментора?


class Lecturer(Mentor):
    path = "log_4.log"

    @logger(path)
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.ratings = {}
    pass


class Reviewer(Mentor):
    path = "log_4.log"

    @logger(path)
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def test_1():

    best_student = Student('Ruoy', 'Eman', 'your_gender')
    best_student.courses_in_progress += ['Python']

    cool_lector = Lecturer('Lector', 'Surnameov')
    cool_lector.courses_attached += ['Python']

    cool_reviewer = Reviewer('Reviewer', 'Patronymickovich')
    cool_reviewer.courses_attached += ['Python']

    cool_reviewer.rate_hw(best_student, 'Python', 10)

    best_student.rate_lector(cool_lector, 'Python', 10)

    print(best_student.grades)
    print(cool_lector.ratings)

if __name__ == '__main__':
    test_1()
    # test_2()