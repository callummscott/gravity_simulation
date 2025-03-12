import pytest

from src.classes.symmetric import Symmetric


@pytest.mark.parametrize( "n", [1, 4, 6, 7, 12, 13, 20, 100] )
def test_symmetric__new___n(n):
    assert Symmetric(n).size == n**2
    assert Symmetric(n).shape == (n,n)


@pytest.mark.parametrize( "n", ["test", (1, 1), [], 2.3] )
def test_symmetric__new__type_error(n):
    with pytest.raises(TypeError):
        Symmetric(n)


@pytest.mark.parametrize( "n", [0, -5, -1, -100] )
def test_symmetric__new__value_error(n):
    with pytest.raises(ValueError):
        Symmetric(n)


@pytest.mark.parametrize(
    "n, i, j, value",
    [
        (5, 3, 4, 10.2),
        (7, 1, 2, 3.221),
        (8, 2, 4, 100.001),
        (11, 6, 5, 7_654),
        (12, 5, 5, 0),
        (20, 10, 10, 0)
    ]
)
def test_symmetric__setitem__(n, i, j, value):
    matrix = Symmetric(n)
    matrix[i, j] = value
    assert matrix[i, j] == value
    assert matrix[j, i] == value
    for i in range(n):
        assert matrix[i, i] == 0
