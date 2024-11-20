import pytest

from Fractal.fractal import Tree, SmoothPosition, map_range

def test_map_range():
    assert map_range(5, 0, 10, 0, 100) == 50
    assert map_range(0, 0, 10, 0, 100) == 0
    assert map_range(10, 0, 10, 0, 100) == 100

def test_smooth_position_initialization():
    pos = SmoothPosition()
    assert pos.current_x == 0
    assert pos.current_y == 0
    assert pos.history == []

def test_tree_initialization():
    tree = Tree(100, 100, 200, 0.65, 90, 20)
    assert tree.x == 100
    assert tree.y == 100
    assert tree.is_growing == True 