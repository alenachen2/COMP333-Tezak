def count(mask):
    '''
    Counts the number of cells by using the number of labels in the mask and subtracting one label 
    for the background.
    Input:
        mask: a list that holds the labels corresponding to each region of interest (ROI)
    Output: the number of cells.
    '''
    return(len(mask) - 1)