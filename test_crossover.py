"""Project unit tests."""
import main


def test_crossover():
    """Test main's crossover function."""
    x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    y = ['b', 'e', 'f', 'h', 'a', 'd', 'g', 'c']
    assert main.crossover(x, y, 2, 5) == (
        ['d', 'e', 'f', 'h', 'a', 'g', 'b', 'c'],
        ['h', 'a', 'c', 'd', 'e', 'g', 'b', 'f']
    )
