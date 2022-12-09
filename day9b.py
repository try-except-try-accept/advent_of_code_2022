from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy

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
R 2///1
---R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20///36"""

DEBUG = False

def display(visited, rope):

    if not DEBUG:
        return

    min_x = 0
    max_x = 6
    min_y = -4
    max_y = 5

    if big:   # dodgy
        max_x = 13
        max_y = 7
        min_y = -19
        min_x = -13

    out = ""
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            pos = (x, y)

            for index, knot in enumerate(rope):
            
                if pos == (knot.x, knot.y):
                    out += str(knot)
                    break
            else:
                if pos in visited:
                    out += "#"
                else:
                    out += "."

        out += "\n"

    p.bugprint(out)
    p.buginput()
    



class Knot:

    def __init__(self, i):

        self.x = 0
        self.y = 0
        self.direction = None
        self.next = None
        self.is_head = i == 0
        self.last = None
        self.code = "H" if i == 0 else str(i)

    def __repr__(self):
        return self.code

    def get_coords(self):
        return f"{self.x}, {self.y}"

    def two_away(self):
        nk = self.next
        return abs(self.x - nk.x) == 2 or abs(self.y - nk.y) == 2


    def check_congestion(self, d):
        nk = self.next
            
        if abs(self.x - nk.x) == 1 == abs(self.y - nk.y):
            p.bugprint("diagonal", end=" ")
            return True
        if (self.direction == "R" or d == "R") and self.x+1 == nk.x and self.y == nk.y:
            p.bugprint("rightward", end=" ")
            return True
        if (self.direction == "L" or d == "L") and self.x-1 == nk.x and self.y == nk.y:
            p.bugprint("leftward", end=" ")
            return True
        if (self.direction == "U" or d == "U") and self.y-1 == nk.y and self.x == nk.x:
            p.bugprint("upward", end=" ")
            return True
        if (self.direction == "D" or d == "D") and self.y+1 == nk.y and self.x == nk.x:
            p.bugprint("downward", end=" ")
            return True
        
        return False

    def move(self, d):

        continue_move = True
        
        self.last = (self.x, self.y)
        if self.is_head:
            if d == "U":    self.y -= 1
            if d == "D":    self.y += 1
            if d == "L":    self.x -= 1
            if d == "R":    self.x += 1
            
        else:

            nk = self.next
            
            # if going in same direction
            # assume next knot's last position

            p.bugprint("Moving", str(self))
            

            if self.check_congestion(d):
                p.bugprint("congestion")
                continue_move = False
            else:                
                if self.two_away():
                    if nk.x > self.x:
                        self.x += 1
                    elif nk.x < self.x:
                        self.x -= 1                        
                    if nk.y > self.y:
                        self.y += 1
                    elif nk.y < self.y:
                        self.y -= 1
                elif self.x != nk.x and self.y != nk.y:
                    self.x, self.y = nk.last

            
        
        self.direction = d
        return continue_move

def solve(data):
    count = 0


    visited = set()

    rope = [Knot(i) for i in range(10)]

    for i in range(9, 0, -1):
        rope[i].next = rope[i-1]

 
    for row_num, row in enumerate(data):
        direction, turns = row.split()
        turns = int(turns)
        
        for i in range(turns):
            for knot in rope:

                p.bugprint(list(knot.get_coords() for knot in rope))

                if row_num >= 0:
                    display(visited, rope)
                continue_move = knot.move(direction)
         
            
                if continue_move == False:
                    break
                ## END ROPE LOOP
                visited.add(rope[-1].get_coords())
                p.bugprint(visited)
            
        ## END TURN LOOP
        display(visited, rope)

    ## END ROW LOOP

    
    display(visited, rope)
    return len(visited)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    big = True
    if p.check(TESTS, solve):
        
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
