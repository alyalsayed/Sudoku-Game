import random
import time


def create_board(level):
    if level == 'easy':
        puzzle = random_puzzle(random.randint(30, 40))
    elif level == 'medium':
        puzzle = random_puzzle(random.randint(25, 30))
    elif level == 'hard':
        puzzle = random_puzzle(random.randint(20, 25))
    elif level == 'extreme':
        puzzle = random_puzzle(random.randint(17, 20))
    else:
        print('Invalid Level')
    return puzzle


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. """
    # squares  ['A1', 'A2', 'A3' ... A9, B1, B2, B3 ... B9, C1, C2, C3 ... C9, ... I9]
    values = dict((s, digits) for s in squares)
    # {'A1': '123456789', 'A2': '123456789', 'A3': '123456789' ...}
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s]) == 1 else '.' for s in squares)
    return random_puzzle(N)  # Give up and make a new puzzle


def shuffled(seq):

    # "Return a randomly shuffled copy of the input sequence."

    test_list = list(seq)
    for i in range(len(test_list)-1, 0, -1):
        # Pick a random index from 0 to i
        j = random.randint(0, i + 1)

        # Swap arr[i] with the element at random index
        test_list[i], test_list[j] = test_list[j], test_list[i]
    return test_list


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], []))-set([s]))
             for s in squares)

# The parse_grid function converts the grid to a dictionary of possible values.


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    # To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  # (Fail if we can't assign d to square s.)
    return values
# extracts the important values which are digits, 0, and .


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


# the assign function is used to assign the value to the square and eliminate the value from the peers.
#  If anything goes wrong, the function returns False.

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

# The all() function returns True if all items in an iterable are true, otherwise it returns False.
# The eliminate function will eliminate values that we know can't be a solution using the two strategies


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


def solve(grid): return search(parse_grid(grid))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


#  some function used to check if an attempt succeeds to solve the puzzle.

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e:
            return e
    return False

# The display function will display the result after calling parse_grid.


def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print()

# check solution and is_solved do the same thing

def check_solution(solution):
    # check rows of solution
    for row in solution:
        if len(row) != len(set(row)):
            return False
    # check columns of solution
    for col in range(len(solution)):
        column = []
        for row in solution:
            column.append(row[col])
        if len(column) != len(set(column)):
            return False
    # check 3x3 squares of solution
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            square = []
            for r in range(row, row+3):
                for c in range(col, col+3):
                    square.append(solution[r][c])
            if len(square) != len(set(square)):
                return False
    return True


def is_solved(values):
    # "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)
