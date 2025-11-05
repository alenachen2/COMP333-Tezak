#user test

from cell_identification import classify_cell, count_cells

def test_classify_cell_red():
    cell = {"color": "red"}
    assert classify_cell(cell) == "Cell Identified"

def test_classify_notcell():
    cell = {"color": "blue"} 
    assert classify_cell(cell) == "Not a Cell"

def test_count_cells():
    cells = [{"color": "red"}, {"color": "blue"}, {"color": "red"}]
    result = count_cells(cells)
    assert result == {"Cells Identified": 2, "Cells Not Identified": 1}

