from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 22
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5///6032"""

DEBUG = True


RDLU = ((1, 0),
        (0, 1),
        (-1, 0),
        (0, -1))
        


def move(x, y, w, h, board_map, num, dir_symbol, path_record):
    last_actual_x, last_actual_y = x, y

    vector = RDLU[">V<^".index(dir_symbol)]

    path_record[(x, y)] = dir_symbol

    while num > 0:
        


        nx = (x + vector[0]) % w             # wrap round x axis
        ny = (y + vector[1]) % h             # wrap round y axis



        if board_map[ny][nx] == "#":         # if hit brick, last pos was final pos
            return "", last_actual_x, last_actual_y

        elif board_map[ny][nx] == " ":       # if hit space, teleport!
            pass

        else:                                # else hit free space ., counts as a move
            num -= 1
            last_actual_x, last_actual_y = nx, ny
            path_record[(nx, ny)] = dir_symbol


        x, y = nx, ny

            
        
    return "", x, y

        
        
def display(board_map, path_record):
    out = ""
    for y, row in enumerate(board_map):
        for x, cell in enumerate(row):
            direction = path_record.get((x, y))
            if direction is not None:
                cell = direction
            out += cell
        out += "\n"
    print(out)
        
    

def solve(data):
    count = 0


    WIDTH = len(max(data[:-1], key=len))
    board_map = data[:-2]
    path = list(data[-1])

    board_map = [list(row.ljust(WIDTH, " ")) for row in board_map]

    orientation = 0

    x, y = board_map[0].index("."), 0

    HEIGHT = len(board_map)

    path_record = {}
    
    num = ""
    dir_symbol = ">"
    while path:
        

        next_char = path.pop(0)

        if next_char in "LR":

            num, x, y = move(x, y, WIDTH, HEIGHT, board_map, int(num), dir_symbol, path_record)
            
            if next_char == "L":
                orientation = ((orientation - 1) % 4)
            else:
                orientation = ((orientation + 1) % 4)

            dir_symbol = ">V<^"[orientation]
            continue

        num += next_char

    if num:
        num, x, y = move(x, y, WIDTH, HEIGHT, board_map, int(num), dir_symbol, path_record)


    path_record[(x, y)] = "☺"

    final_row = y + 1
    final_col = x + 1
    display(board_map, path_record)
    
    return sum([1000 * final_row, 4 * final_col, orientation])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
