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

def display_pix_info(cycle=0, sprite_pos=0, crt=0, last_row="", current_row="", task="", x=0):

    draw_sprite = ("." * (sprite_pos - 2))
    draw_sprite += "###"
    draw_sprite += ("." * (40 - sprite_pos - 1))

    p.bugprint(f'''Sprite position: {draw_sprite}

Start cycle   {cycle-1}: begin executing {task}
During cycle  {cycle-1}: CRT draws pixel in position {crt-1}
Current CRT row: {last_row}

During cycle  {cycle}: CRT draws pixel in position {crt}
Current CRT row: {current_row}
End of cycle  {cycle}: finish executing {task} (Register X is now {x})''')


def draw(img, crt, x):
    pixel = "."
    crt_range = list(range(crt[0]-1, crt[0]+2))
    if x in crt_range:
        
        pixel = "#"

    img[-1] += pixel

def solve(data):
    pc = 0
    x = 1
    signal_strength = 0
    STRENGTH_INCREASE = 40
    cycle_wanted = 20
    data = data * 10
    LIMIT = 240
    cycle = 1
    task_q = [0]
    img = [""]
    LEFT_BOUND = 0
    RIGHT_BOUND = 39

    crt = [0, 0]

    while True:
        instruction = data.pop(0)        
        p.bugprint(f"During cycle {cycle} x is {x}")

        draw(img, crt, x)

        if cycle == LIMIT:
            for row in img:
                print(row)

        if instruction.startswith("addx"):
            _, amt = instruction.split()
            amt = int(amt)
            tasks = [amt, 0]
        else:
            tasks = [0]

        task_q += tasks
        next_task = task_q.pop(0)
        x += next_task

        begin = ("addx" if next_task != 0 else "noop") + " " + str(next_task)        
        
        p.bugprint(f"After cycle {cycle} x is {x}")
             

        crt[0] += 1
        if crt[0] > RIGHT_BOUND:
            crt = [0, crt[1]+1]
            img.append("")
        
        if cycle % 2 == 0:
            display_pix_info(cycle=cycle, sprite_pos=last_x, crt=crt[0], last_row=last_row,
                             current_row=img[-1], task=begin, x=x)
            p.buginput()
        
    
        cycle += 1
        last_x = x
        last_begin = begin
        last_row = img[-1]


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if True: #p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
