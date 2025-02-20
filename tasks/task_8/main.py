# Задача 1: Найти первое вхождение 20 и заменить его на 200
from typing import List


from tasks.task_8.generator_data import generate_numbers1, generate_strings, generate_numbers2, generate_numbers3


def task_1(numbers: List[int]) -> List[int]:
    if 20 in numbers:
        index = numbers.index(20)
        numbers[index] = 200
    return numbers


# Задача 2: Удалить пустые строки из списка строк
def remove_empty_strings(strings: List[str]) -> List[str]:
    return list(filter(lambda x: x != '' and x is not None, strings))

def remove_empty_strings_2(strings):
    return [string for string in strings if string != ""]


# Задача 3: Превратить список чисел в список их квадратов
def square_numbers(numbers: List[int]) -> List[int]:
    return [x ** 2 for x in numbers]


# Задача 4: Удалить все вхождения числа 20 из списка
def remove_all_20(numbers: List[int]) -> List[int]:
    return [x for x in numbers if x != 20]


def main():
    # Выполнение и вывод результатов
    print("Задача 1:")
    numbers1 = generate_numbers1()
    print("Исходный список:", numbers1)
    print("После замены первого 20 на 200:", task_1(numbers1))
    print()

    print("Задача 2:")
    strings = generate_strings()
    print("Исходный список:", strings)
    print("Без пустых строк:", remove_empty_strings(strings))
    print("Без пустых строк вторым способом:", remove_empty_strings_2(strings))
    print()

    print("Задача 3:")
    numbers2 = generate_numbers2()
    print("Исходный список:", numbers2)
    print("Список квадратов:", square_numbers(numbers2))
    print()

    print("Задача 4:")
    numbers3 = generate_numbers3()
    print("Исходный список:", numbers3)
    print("Без всех 20:", remove_all_20(numbers3))


if __name__ == "__main__":
    main()
