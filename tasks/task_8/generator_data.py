import random
from typing import List


# Генерация данных для задачи 1
def generate_numbers1() -> List[int]:
    # Список из 5-10 случайных чисел от 10 до 40, с шансом включения 20
    length = random.randint(5, 10)
    return [random.choice([20] + [random.randint(10, 40) for _ in range(5)]) for _ in range(length)]


# Генерация данных для задачи 2
def generate_strings()-> List[str]:
    # Список из 5-10 элементов: случайные слова, пустые строки и None
    words = ["apple", "banana", "cat", "dog", "elephant"]
    length = random.randint(5, 10)
    return [random.choice(words + [None, ""]) for _ in range(length)]

# Генерация данных для задачи 3
def generate_numbers2()-> List[int]:
    # Список из 5 случайных чисел от 1 до 10
    return [random.randint(1, 10) for _ in range(5)]


# Генерация данных для задачи 4
def generate_numbers3()-> List[int]:
    # Список из 5-10 случайных чисел от 10 до 30
    length = random.randint(5, 10)
    generated_mas =  [random.choice([20] + [random.randint(10, 30) for _ in range(5)]) for _ in range(length)]
    generated_mas.append(20)
    return generated_mas
