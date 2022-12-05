from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 5
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2///CMZ
"""

DEBUG = True


def solve(data):
    count = 0

    for i, line in enumerate(data):


        if line.replace(" ", "").isdigit():

            num_stacks = int(line.strip()[-1])
            sep = i
            break

    stacks = [[] for i in range(num_stacks)]

    

    for line in data[:sep]:
        for i in range(1, num_stacks*4, 4):

            if line[i] != " ":

                crate = line[i]
                stacks[i//4].insert(0, crate)


    print(stacks)

    input()

        
            
    for line in data[sep+2:]:
        line = line.split()

        amt = int(line[1])
        from_stack = int(line[3])
        to_stack = int(line[5])


        for i in range(amt):
            stacks[to_stack-1].append(stacks[from_stack-1].pop())


    msg = ""
    for i in stacks:
        msg += i.pop(-1)
        

        
    

    return msg




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
