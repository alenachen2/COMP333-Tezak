from cell_identification import classify_cell 
from cell_identification import count_cells

def test_classify_cell_red():
    '''
    Test a case where the input of classify_cell is a cell. 
    Expected output: true
    '''
    cell = {"color": "red"}
    assert classify_cell(cell) == "Cell Identified"


def test_classify_notcell():
    '''
    Test a case where the input for classify_cell is not a cell. 
    Expected output: false
    '''
    cell = {"color": "blue"} 
    assert classify_cell(cell) == "Not a Cell"


def test_count_cells():
    '''
    Test count_cells given a list of cells where two are cells and one is not.
    Expected output: 2, 1
    '''
    cells = [{"color": "red"}, {"color": "blue"}, {"color": "red"}]
    result = count_cells(cells)
    assert result == {"Cells Identified": 2, "Cells Not Identified": 1}

