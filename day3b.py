from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, True #rotate, cast int

DAY = 3
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw///70
"""

DEBUG = True


def solve(data):
    count = 0

    for i in range(0, len(data), 3):
        d = [set(x) for x in [data[i], data[i+1], data[i+2]]]
 
        shared = d[0].intersection(d[1]).intersection(d[2])
        for s in shared:
            x = ord(s)
            if x >= 97:
                x -= 96
            else:
                x -= (65-27)
            #print("shared", s, x)
            count += x
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
