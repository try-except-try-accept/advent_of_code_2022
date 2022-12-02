from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 2
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """A Y
B X
C Z///12"""



DEBUG = True


def solve(data):
    goals =  "XYZ"
    you = "ABC"
    OPTIONS = 3   

    total = 0
    for row in data:        
        you_code, goal = row.split()
        
        your_choice = you.index(you_code)
        total += 1 # index offset
        if goal == "Y":
            total += 3 + (your_choice)
        elif goal == "X":
            total += ((your_choice - 1) % OPTIONS)
        else:
            total += 6 + ((your_choice + 1) % OPTIONS)

    
    return total


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
