from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 10
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop///13140"""

DEBUG = False





def solve(data):
    pc = 0
    x = 1
    signal_strength = 0
    STRENGTH_INCREASE = 40
    cycle_wanted = 20
    data = data * 10
    LIMIT = 220
    cycle = 1
    task_q = [0]

    while True:
        instruction = data.pop(0)   

        p.bugprint(f"During cycle {cycle} x is {x}")

        if cycle == cycle_wanted:
            signal_strength += (cycle * x)
            print(f"register X has the value {x}, so the signal strength is {cycle} * {x} = {cycle * x}")
            cycle_wanted += STRENGTH_INCREASE
            p.buginput()

        if cycle == LIMIT:
            return signal_strength            
        
        if instruction.startswith("addx"):
            _, amt = instruction.split()
            amt = int(amt)
            tasks = [amt, 0]
        else:
            tasks = [0]

        task_q += tasks

        x += task_q.pop(0)

        p.bugprint(f"After cycle {cycle} x is {x}")
        
        cycle += 1


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
