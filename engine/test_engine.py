import pytest
import numpy as np
from engine import Engine
from constants import Spaces


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

def test_toggle_flag():
    e = Engine(10, 10, 10)
    orig_space = e.get_display_board()[0, 0]
    e.toggle_flag(0, 0)
    assert e.get_display_board()[0, 0] == Spaces.FLAG
    e.toggle_flag(0, 0)
    assert e.get_display_board()[0, 0] == orig_space

def test_click_bomb():
    e = Engine(10, 10, 50)
    for i in range(10):
        for j in range(10):
            if not e.check_location(i, j):
                return
    assert False, "Clicking bomb spaces did not return false."

def test_display_board():
    b1 = np.array([
        [Spaces.BOMB, Spaces.UNKNOWN],
        [Spaces.BOMB, Spaces.BOMB]
    ])
    e = Engine(10, 10, 50)
    e._board = b1
    dboard = e.get_display_board()
    assert dboard[0, 0] == Spaces.UNKNOWN
    assert dboard[0, 1] == Spaces.UNKNOWN
    assert dboard[1, 0] == Spaces.UNKNOWN
    assert dboard[1, 1] == Spaces.UNKNOWN

def test_click_flag():
    e = Engine(10, 10, 1)
    orig_space = e.get_display_board()[0, 0]
    e.toggle_flag(0, 0)
    assert e.get_display_board()[0, 0] == Spaces.FLAG
    e.check_location(0, 0)
    assert e.get_display_board()[0, 0] == orig_space

def test_click_safe():
    b1 = np.array([
        [Spaces.BOMB, Spaces.UNKNOWN],
        [Spaces.BOMB, Spaces.BOMB]
    ])
    e = Engine(10, 10, 1)
    e._board = b1
    e._width = 2
    e._height = 2
    e.check_location(0, 1)
    assert e.get_real_board()[0, 0] == Spaces.BOMB
    assert e.get_real_board()[1, 0] == Spaces.BOMB
    assert e.get_real_board()[1, 1] == Spaces.BOMB
    assert e.get_real_board()[0, 1] == Spaces.THREE

    b2 = np.array([
        [Spaces.UNKNOWN, Spaces.UNKNOWN, Spaces.BOMB],
        [Spaces.UNKNOWN, Spaces.UNKNOWN, Spaces.BOMB],
        [Spaces.UNKNOWN, Spaces.UNKNOWN, Spaces.BOMB]
    ])
    e._board = b2
    e._width = 3
    e._height = 3
    e.check_location(0, 0)
    assert e.get_real_board()[0, 0] == Spaces.ZERO
    assert e.get_real_board()[0, 1] == Spaces.TWO
    assert e.get_real_board()[0, 2] == Spaces.BOMB
    assert e.get_real_board()[1, 0] == Spaces.ZERO
    assert e.get_real_board()[1, 1] == Spaces.THREE
    assert e.get_real_board()[1, 2] == Spaces.BOMB
    assert e.get_real_board()[2, 0] == Spaces.ZERO
    assert e.get_real_board()[2, 1] == Spaces.TWO
    assert e.get_real_board()[2, 2] == Spaces.BOMB
