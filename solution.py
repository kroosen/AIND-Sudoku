import time
from collections import defaultdict
from itertools import combinations
from utils import *

start_time = time.time()

#==============================================================================
# TO THE REVIEWER:
#     
#     I have implemented your suggestions. I'm quite proud that I haven't done the hidden_twins,
#     but instead did hidden_tuples!
#     I'm not really convinced that the modularization has increased the code readability,
#     but I've tried to make it as clean as possible.
#     
#     The only thing I haven't done is the logging. I have never used it.
#     I will definitely learn and try to use it for the next projects, but for lack of time I have skipped it.
#     I do know assertions, and will use them from next project on as well!
#
#     Thanks for your awesome feedback! :)
#==============================================================================


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
        for digit in digits:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1 and len(values[dplaces[0]]) > 1:
                values = assign_value(values, dplaces[0], digit)                      
    return values

def naked_twins(values):
    """ For grading purposes """
    return naked_tuples(values)

def naked_tuples(values):
    """ Eliminate values using the naked tuples strategy.
    
    If, within a unit, we can identify x boxes that all hold the same and exactly x possibilities, we can rule out
    these possibilities from all other boxes within the unit.
    """
    def identify_naked_tuples(values, unit):
        possibilities = defaultdict(list)
        for box in unit:
            possibilities[values[box]].append(box)
        return {p: possibilities[p] for p in possibilities if len(p) == len(possibilities[p]) > 1}
        
    def eliminate_nt_values(values, unit, naked_tuples):
        for b in unit:
            if len(values[b]) > 1:  # Only check the yet unsolved boxes
                for nt in naked_tuples:
                    if b not in naked_tuples[nt]:
                        for digit in nt:
                            values[b] = values[b].replace(digit, '')
                        if len(values[b]) == 1:
                            # If only 1 possibility remains, assign it using the provided function for visualization purposes
                            values = assign_value(values, b, values[b])
        return values
    
    for unit in unitlist:
        # Step 1: identify the naked_tuples
        naked_tuples = identify_naked_tuples(values, unit)
        # Step 2: eliminate all possibilities from the naked tuple's values from the other boxes in the unit
        values = eliminate_nt_values(values, unit, naked_tuples)
        
    return values

def hidden_tuples(values):
    """
    For every combination of existing possibilities within a unit, count the number of yet unsolved boxes that have this combination.
    If the length of the combination exactly matches this number of boxes and none of the other boxes contain a digit of this combination,
    we have found a hidden twin.
    """
    def make_combination_dict(values, unit, cs):
        ht_candidates = defaultdict(list)
        for combination in cs:
            for box in unit:
                #if len(values[box]) > 1:
                d_in_box = [d in values[box] for d in combination]
                if any(d_in_box):  # none of the other boxes may contain this digit:
                    ht_candidates[combination].append(box)
        return ht_candidates
                    
    def eliminate_ht_values(values, hidden_tuples):
        for t in hidden_tuples:
            for b in hidden_tuples[t]:
                for digit in values[b]:
                    if digit not in t:
                        values[b] = values[b].replace(digit, '')
                    if len(values[b]) == 1:
                        # If only 1 possibility remains, assign it using the provided function for visualization purposes
                        values = assign_value(values, b , values[b])
        return values
    
    for unit in unitlist:
        # Step 1: define all possible combinations (sorted order) of length 2
        cs = list()
        for i in range(2,9):
            cs += [''.join(c) for c in combinations(digits, i)]

        # Step 2: Make a dict of all boxes per combination that contain at least one digit of the combination.
        ht_candidates = make_combination_dict(values, unit, cs)
                        
        # Step 3: if the # of boxes exactly matches the # of digits in a combination, we have a hidden tuple.
        # Of all the candidates that contain at least one digit of the combination,
        # now each candidate must contain all combination digits
        hidden_tuples = {c: ht_candidates[c] for c in ht_candidates
                         if len(c) == len(ht_candidates[c]) > 1
                         if all([d in values[b] for d in c for b in ht_candidates[c]])
                         }

        # Step 4: eliminate all values in the hidden tuple that are not part of the shared values
        values = eliminate_ht_values(values, hidden_tuples)
    
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
        values = naked_tuples(values)  # instead of values = naked_twins(values)
        values = hidden_tuples(values) # new feature, also working for triples, quadruples, ...
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
    print('Test 1:')
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    if solve(diag_sudoku_grid):
        print('SOLUTION FOUND')
        print()
#==============================================================================
#         try:
#             print('The calculations took %s seconds' % (time.time() - start_time))
#             from visualize import visualize_assignments
#             visualize_assignments(assignments)
#         except SystemExit:
#             pass
#         except:
#             print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
#==============================================================================
    else:
        print ('No solution found.')
    
    print('Test 2:')
    grid = grid_values('2...4.1.79.....24.84.2..56.7124983566.....4..5946...2.45.3.79121..9.4.353.9.1...4')
    print('Grid before hidden tuples operation:')
    display(grid)
    print()
    print('Grid after hidden tuples operation:')
    display(hidden_tuples(grid))