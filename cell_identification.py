class cell:
    def __init__(self):
        self.data = []

#User test function 
def classify_cell(cell): 
    if cell["color"] == "red": 
        return "Cell Identified"
    else: 
        return "Not a Cell"

def count_cells(cell_list): 
    count_cell = 0 
    count_notcell = 0
    for cell in cell_list: 
        if classify_cell(cell) == "Cell Identified": 
            count_cell += 1
        else: 
            count_notcell += 1
    return{"Cells Identified": count_cell, "Cells Not Identified": count_notcell}
