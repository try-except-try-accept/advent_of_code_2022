from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 6
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """mjqjpqmgbljsphdztnvjfqwrcgsmlb///19
---
bvwbjplbgvbhsrlpgdmjqwftvncz///23
---
nppdvjthqldpwncqszvftbrmjlhg///23
---
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg///29
---
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw///26
---"""
DEBUG = True



def solve(data):
    count = 0
    data = data[-1]
    CHUNK_SIZE = 14
    
    for i, char in enumerate(data):

        chunk = data[i:i+CHUNK_SIZE]
        
        if len(set(chunk)) != CHUNK_SIZE:            
            continue
        else:
            return i + CHUNK_SIZE







if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
