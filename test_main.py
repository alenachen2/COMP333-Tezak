from cell_counting import count

def test_count_basic():
    mask = [0, 1, 2, 3]
    assert count(mask) == 3

def test_count_empty_mask():
    mask = []
    assert count(mask) == -1

def test_count_only_background():
    mask = [0]
    assert count(mask) == 0

def test_count_multiple_same_label():
    mask = [0, 1, 1, 2, 2, 3]
    assert count(mask) == 5