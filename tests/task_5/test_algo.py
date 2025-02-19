import pytest

from tasks.task_5.algo import calculate, evaluate_rpn, shunting_yard, tokenize


def test_tokenize_simple():
    assert tokenize("1 + 2 + 3") == ['1', '+', '2', '+', '3']
    assert tokenize('1*(2-3)') == ['1', '*', '(', '2', '-', '3', ')']

def test_tokenize_with_trigonometry():
    assert tokenize("3.14 + 2 * (sin(0.5) - 1)") == ['3.14', '+', '2', '*', '(', 'sin', '(', '0.5', ')', '-', '1', ')']

def test_shunting_yard():
    assert shunting_yard("3 + 4 * 2 / (1 - 5)^2") == ['3', '4', '2', '*', '1', '5', '-', '2', '^', '/', '+']

def test_evaluate_rpn():
    assert evaluate_rpn(['3', '4', '2', '*', '1', '5', '-', '2', '^', '/', '+']) == 3.5

def test_simple_addition():
    assert calculate("2 + 3") == 5

def test_simple_subtraction():
    assert calculate("5 - 3") == 2

def test_simple_multiplication():
    assert calculate("4 * 3") == 12

def test_simple_division():
    assert calculate("10 / 2") == 5

def test_exponentiation():
    assert calculate("2 ^ 3") == 8

def test_complex_expression():
    assert calculate("3 + 5 * (2 - 8)^2 / 4") == 48

def test_floating_point():
    assert abs(calculate("3.14 * 2") - 6.28) < 1e-6

def test_precedence():
    assert calculate("2 + 3 * 4") == 14

def test_associativity():
    assert calculate("8 - 3 - 2") == 3

def test_parentheses():
    assert calculate("(2 + 3) * 4") == 20


def test_invalid_expression_open_bracket():
    with pytest.raises(ValueError):
        calculate("2 + (3 * 4")

def test_invalid_expression_closed_bracket():
    with pytest.raises(ValueError):
        calculate("2 + 3 * 4)")

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("1 / 0")
