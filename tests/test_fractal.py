import pytest
import sys
import os

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fractal import Tree, SmoothPosition, map_range

def test_tree_initialization():
    """Prueba la inicialización básica de un árbol"""
    tree = Tree(100, 100, 200, 0.65, 90, 20)
    assert tree.x == 100
    assert tree.y == 100

def test_tree_properties():
    """Prueba las propiedades del árbol"""
    tree = Tree(100, 100, 200, 0.65, 90, 20)
    assert tree.size == 200
    assert tree.decay == 0.65 