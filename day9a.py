from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

big = False

DAY = 9
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2///13"""

DEBUG = False

def display(visited, snake):

    if not DEBUG:
        return

    min_x = 0
    max_x = 6
    min_y = -4
    max_y = 1

    if big:   # dodgy
        max_x *= 5
        max_y *= 15
        min_y -= 0
        min_x -= 25

    hx, hy = snake[0]
    tx, ty = snake[1]
    print(snake)

    out = ""
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            pos = (x, y)
            
            if pos == (hx, hy):
                out += "H"
            elif pos == (tx, ty):
                out += "T"
            elif pos in visited:
                out += "#"
            else:
                out += "."

        out += "\n"

    p.bugprint(out)

    

def solve(data):
    count = 0


    visited = set()

    
    
    snake = [[0, 0], [0, 0]]

    
    first = True
    for row in data:

        p.bugprint("==", row, "==")

        d, amt = row.split()
        amt = int(amt)
      
        
        for i in range(amt):
            tail_move = True
            head = snake[0]
            tail = snake[1]

            if d == "L":
                head[0] -= 1
            elif d == "R":
                head[0] += 1
            elif d == "U":
                head[1] -= 1
            else:
                head[1] += 1

            # no need to move tail

            horiz = d in "LR"
            vert = d in "UD"
            x_same = head[0] == tail[0]
            y_same = head[1] == tail[1]
            
            if first or x_same and horiz or y_same and vert:
                first = False                
                tail_move = False

            # move tail

            if tail_move:
                    
                if d == "L":
                    tail[0] -= 1                   
                elif d == "R":
                    tail[0] += 1                
                elif d == "U":
                    tail[1] -= 1
                else:
                    tail[1] += 1
                
                if horiz:
                    row_diff = head[1] - tail[1]                    
                    if row_diff == 1:
                        tail[1] += 1
                    elif row_diff == -1:
                        tail[1] -= 1
                else:
                    col_diff = head[0] - tail[0]
                    if col_diff == 1:
                        tail[0] += 1
                    elif col_diff == -1:
                        tail[0] -= 1

            
            if tail == head:                
                snake[1] = list(last_tail)
            else:               
                visited.add(tuple(tail))


            display(visited, snake)


            last_tail = tuple(tail)
    

    return len(visited)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        big = True
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
