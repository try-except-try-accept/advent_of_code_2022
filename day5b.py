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
move 1 from 1 to 2///MCD
"""

DEBUG = True


def solve(data):
    count = 0

    for i, line in enumerate(data):
        if line.replace(" ", "").isdigit():     # is this line only digits?
            num_stacks = int(line.split()[-1])  # last number represents num of stacks
            sep = i                             # end of stack data
            break

    stacks = [[] for i in range(num_stacks)]    # create empty stacks
    

    stack_data = data[:sep]
    mov_data = data[sep+2:]

    STACK_WIDTH = 4

    for line in stack_data:                     
        for i in range(1, num_stacks*STACK_WIDTH, STACK_WIDTH): # loop through crate code character positions

            if line[i] != " ":                                  # is crate code present?
                crate = line[i]
                stacks[i//STACK_WIDTH].insert(0, crate)         # if so, add to bottom of stack (top parsed first)
        
            
    for line in mov_data:
        
        line = line.split()

        amt = int(line[1])
        from_stack = int(line[3]) - 1                       # account for 0-based Python indices
        to_stack = int(line[5]) - 1

        move_crates = []
        for i in range(amt):
            move_crates.append(stacks[from_stack].pop())    # take off top crate and get ready to move

        for crate in reversed(move_crates):                 # crates added in reverse order - equivalent logic to multiple moved at once
            stacks[to_stack].append(crate)


    msg = ""
    for stack in stacks:            # msg = top crate of each stack
        msg += stack.pop(-1)
        

        
    

    return msg




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
