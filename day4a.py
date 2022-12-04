from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 4
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8///2
"""

DEBUG = True


def solve(data):
    count = 0

    for row in data:
        pair1, pair2 = row.split(",")

        p1, p2 = map(int, pair1.split("-"))        
        p3, p4 = map(int, pair2.split("-"))


        if p1 >= p3 and p2 <= p4 or p3 >= p1 and p4 <= p2:
            count += 1

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
