import pytest
from src.classes.symmetric import Symmetric

def test_symmetric__new__():

    valid_values = [1, 4, 6, 7, 12, 13, 20, 100]
    for n in valid_values:
        assert Symmetric(n).size == n**2
        assert Symmetric(n).shape == (n,n)

    type_error_values = ["test", (1,1), [], 2.3]
    with pytest.raises(TypeError):
        for value in type_error_values:
            Symmetric(value)

    value_error_values = [0, -5, -1, -100]
    with pytest.raises(ValueError):
        for value in value_error_values:
            Symmetric(value)


def test_symmetric__setitem__():
    # n, i, j, value
    class ExampleInputs:
        def __init__(self, n, i, j, value):
            self.n = n
            self.i = i
            self.j = j
            self.value = value
    
    examples = [
        ExampleInputs(5, 3, 4, 10.2),
        ExampleInputs(7, 1, 2, 3.221),
        ExampleInputs(8, 2, 4, 100.001),
        ExampleInputs(11, 6, 5, 7_654),
        ExampleInputs(12, 5, 5, 0),
        ExampleInputs(20, 10, 10, 0)
    ]

    for example in examples:
        matrix = Symmetric(example.n)
        matrix[example.i, example.j] = example.value
        assert matrix[example.i, example.j] == example.value
        # Check that values are symmetric
        assert matrix[example.i, example.j] == matrix[example.j, example.i]
        # Check that the diagonal values are all 0
        for i in range(example.n):
            assert matrix[i, i] == 0

