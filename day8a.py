from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 8
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """30373
25512
65332
33549
35390///21"""

DEBUG = True

def display(data, visible):
    for y in range(len(data)):
        for x in range(len(data[y])):
            tree = data[y][x]
            if (x, y) in visible:
                print(tree, end="")
            else:
                print(".", end="")
        print()

def check_tree(biggest, visible, x, y, data):
    this = data[y][x]
    if biggest is None or this > biggest:
        biggest = this
        visible.add((x, y))
 
    return biggest, visible
  

    
    


def solve(data):
    count = 0

    

    W = len(data[0])
    H = len(data)

    data = [list(map(int, d)) for d in data]


    visible = set()

    
    # for each column
    for x in range(W):
        biggest = None
        # check each tree in column down
        for y in range(H):
            biggest, visible = check_tree(biggest, visible, x, y, data)

    # for each column
    for x in range(W):
        biggest = None
        # check each tree in column up
        for y in range(H-1, -1, -1):
            biggest, visible = check_tree(biggest, visible, x, y, data)

    # for each row
    for y in range(H):
        biggest = None
        # check each tree in column rightwards
        for x in range(W):    
            biggest, visible = check_tree(biggest, visible, x, y, data)

    # for each row
    for y in range(H):
        biggest = None
        # check each tree in column leftwards
        for x in range(W-1, -1, -1):
            biggest, visible = check_tree(biggest, visible, x, y, data)
 

    return len(visible)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
