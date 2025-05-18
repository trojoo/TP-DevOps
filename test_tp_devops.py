import pytest
from tp_devops import suma, resta, multiplicacion, division

def test_suma():
    assert suma(2, 3) == 5

def test_resta():
    assert resta(5, 3) == 2

def test_multiplicacion():
    assert multiplicacion(2, 3) == 6

def test_division():
    assert division(6, 3) == 2