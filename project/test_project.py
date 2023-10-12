from project import conway
from project import check_changes
from project import get_pop

def test_conway():
    # Test with a 2x2 grid
    assert conway([[0,1,],[1,1]])==[[1,1],[1,1]]
    assert conway([[0,1],[1,0]])==[[0,0],[0,0]]

   # Test with a 3x3 grid
    assert conway([[0,1,0],[1,1,0],[0,0,0]])==[[1,1,0],[1,1,0],[0,0,0]]
    assert conway([[1,1,0],[1,1,0],[0,0,0]])==[[1,1,0],[1,1,0],[0,0,0]]

    # Test with a 4x4 grid
    assert conway([[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]])==[[0,1,1,0],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
    assert conway([[1,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])==[[1,1,0,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]]


def test_check_changes():
    # Test unchanged
    assert check_changes([[1,0],[0,0]],[[1,0],[0,0]]) == "Stagnation"
    assert check_changes([[1,0,0],[0,0,0],[0,0,1]],[[1,0,0],[0,0,0],[0,0,1]]) == "Stagnation"

    # Test changes
    assert check_changes([[1,1],[1,1]],[[1,1],[1,0]]) == "Go on"
    assert check_changes([[1,1,0],[1,1,0],[0,0,0]],[[1,1,0],[1,0,0],[0,0,0]]) == "Go on"


def test_get_pop():
    # Test sums
    assert get_pop([[0,1,0],[1,1,1],[0,1,0]]) == 5
    assert get_pop([[0,0,0],[1,1,1],[0,0,0]]) == 3
    assert get_pop([[1,1,1],[1,1,1],[1,1,1]]) == 9
    assert get_pop([[0,0,0],[0,0,0],[0,0,0]]) == 0
