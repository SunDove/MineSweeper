import pytest
from engine import Engine


def test_valid_dimensions():
    # Everything here should just not fail
    e = Engine(10, 10, 50)
    e = Engine(10, 10, 0)
    e = Engine(100, 100, 5000)
    e = Engine(100, 100, 0)

def test_mins():
    with pytest.raises(ValueError):
        e = Engine(9, 10, 10)

def test_maxs():
    with pytest.raises(ValueError):
        e = Engine(1000, 10, 10)

def test_bomb_ratio():
    with pytest.raises(ValueError):
        e = Engine(10, 10, 51)
    with pytest.raises(ValueError):
        e = Engine(100, 100, 5001)
