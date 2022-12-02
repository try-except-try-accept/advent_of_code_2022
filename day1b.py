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

10000///45000"""

DEBUG = True


def solve(data):
    print(data)

    data = [int(d) if d != "" else d for d in data ]

    new = [[]]

    for thing in data:
        if thing == "":
            new.append([])
            continue
        new[-1].append(thing)   

    return sum(sorted([sum(n) for n in new], reverse=True)[:3])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
