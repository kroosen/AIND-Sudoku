from collections import defaultdict

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

# row and column names
rows = 'ABCDEFGHI'
cols = '123456789'

# names of all boxes
boxes = cross(rows, cols)

# create units
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [[a+b for a, b in zip('ABCDEFGHI', '123456789')], [a+b for a, b in zip('ABCDEFGHI', '987654321')]]
unitlist = row_units + column_units + square_units + diagonal_units

# dictionaries to identify units and peers for a certain box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# keep track of all the box assignments
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    A solved box contains exactly 1 digit. For all peers of a solved box,
    eliminate this digit from the possibilities
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            if len(values[peer]) == 1:
                values = assign_value(values, peer, values[peer])
    return values

def only_choice(values):
    """
    Loop over all units. Then loop over all digits (1-9). If a certain digit can only be
    placed in 1 box within a unit, assign it and solve the box.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1 and len(values[dplaces[0]]) > 1:
                values = assign_value(values, dplaces[0], digit)                      
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
        
    Loop over all units. If twins can be identified within a unit, change the other boxes
    in this unit by eliminating both digits of the twin's value from the possible values.
    """
    for unit in unitlist:
        # find all twins within the unit
        twins = dict((values[box], (box, box2)) for box in unit for box2 in unit 
                      if box is not box2 
                      if len(values[box]) == 2
                      if values[box] is values[box2])
        # remove the twin's values from the other boxes
        for b in unit:
            for t in twins:
                if b not in twins[t]:
                    values[b] = values[b].replace(t[0], '').replace(t[1], '')
                    if len(values[b]) == 1:
                        values = assign_value(values, b, values[b])
    return values

def reduce_puzzle(values):
    """
    Apply different techniques repeatedly to try and solve the puzzle. When we can
    no longer make progress, return the values.
    If we end up in an invalid state, return False
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Try to solve the puzzle, if we can't, assume a certain state from the possible states and
    continue solving this state recursively. Continue this tree search until a solution is found
    or until we are out of options.
    """
    values = reduce_puzzle(values)
    if values is False: return False
    if all(len(values[s]) == 1 for s in boxes): 
        return values  # The puzzle is solved
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False),
    # return that answer!
    for digit in values[s]:
        new_values = values.copy()
        new_values[s] = digit
        attempt = search(new_values)
        if attempt: return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    if solve(diag_sudoku_grid):
        try:
            from visualize import visualize_assignments
            visualize_assignments(assignments)
        except SystemExit:
            pass
        except:
            print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
    else:
        print ('No solution found.')