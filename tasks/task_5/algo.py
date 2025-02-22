import operator
import re
from typing import List

# приоритет
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

# ассоциативность
# Например, в языке Python большинство операций имеет левую ассоциативность, в то время как возведение в степень правоассоциативно:
associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}


def tokenize(expression: str) -> List[str]:
    """ Токенизация на:
        - \d+\.\d+: Числа с плавающей точкой (например, 3.14)
        - \d+: Целые числа (например, 42)
        - [a-zA-Z]+: Последовательности букв (например, имена функций или переменных)
        - [+\-*/^(),]: Отдельные символы операторов и скобок
    """
    return re.findall(r'\d+\.\d+|\d+|[a-zA-Z]+|[+\-*/^(),]', expression)


def shunting_yard(tokens) -> List[str]:
    """
    https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D1%81%D0%BE%D1%80%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%BE%D1%87%D0%BD%D0%BE%D0%B9_%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%B8
    :param tokens:
    :return: Символы в обратной польской нотации
    """
    output = []  # очередь вывода.
    stack = []

    for token in tokens:
        if token.isdigit() or '.' in token:
            output.append(token)
        elif token.isalpha():  # Функция
            stack.append(token)
        elif token == ',':  # Разделитель аргументов функции
            while stack and stack[-1] != '(':  # сбрасываем, что накопилось в стеке
                output.append(stack.pop())
            if not stack or stack[-1] != '(':
                raise ValueError("Пропущен разделитель аргументов функции или открывающая скобка")
        elif token in precedence:
            while (stack and stack[-1] in precedence and
                   ((associativity[token] == 'L' and precedence[token] <= precedence[stack[-1]]) or
                    (associativity[token] == 'R' and precedence[token] < precedence[stack[-1]]))):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Пропущена открывающая скобка")
            stack.pop()
            if stack and stack[-1].isalpha():
                output.append(stack.pop())

    while stack:
        if stack[-1] == '(':
            raise ValueError("Пропущена закрывающая скобка")
        output.append(stack.pop())

    return output


def evaluate_rpn(rpn_tokens: List[str]) -> int:
    """"
    Вычисления в обратной польской нотации (Reverse Polish notation)
    """

    stack = []
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '^': operator.pow}

    for token in rpn_tokens:
        if token.isdigit() or '.' in token:
            stack.append(float(token))
        elif token in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[token](a, b))

    return stack[0]


def calculate(expression):
    tokens = tokenize(expression=expression)
    rpn = shunting_yard(tokens=tokens)

    return evaluate_rpn(rpn)
