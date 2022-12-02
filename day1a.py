from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 1
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000///24000"""

DEBUG = True


def solve(data):
    count = 0

    
    biggest = 0

    this = 0
    for thing in data:
        
        if thing == "":
            if this > biggest:
                biggest = int(this)
            this = 0
        else:
            this += int(thing)
            last = int(thing)

    

    return max(biggest, this)
    

        
        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
