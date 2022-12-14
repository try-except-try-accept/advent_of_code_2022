from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from os import system

PP_ARGS = False, False #rotate, cast int

DAY = 14
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9///24"""

DEBUG = False

grid = None
ABYSS_BUFFER = 3

sand_x = 0

def create_caves(data):
    global grid, sand_x

    coords = [tuple(map(int, point.split(","))) for point in findall("\d{1,3},\d{1,3}", "\n".join(data))]
    p.bugprint(coords)
    min_x = min(coords)[0] - 5
    max_x = max(coords)[0]

    min_y = min(coords, key=lambda y:y[1])[1]
    max_y = max(coords, key=lambda y:y[1])[1] + ABYSS_BUFFER

    sand_x = 500 - min_x

    grid = [['.' for x in range(max_x-min_x+1)] for y in range(max_y+1)]

    for row in data:
        cave_coords = []
        for point in findall("\d{1,3},\d{1,3}", row):
            cave_coords.append(tuple(map(int, point.split(","))))

        for i in range(1, len(cave_coords)):
            x1, y1 = cave_coords[i-1]
            x2, y2 = cave_coords[i]

            x1 -= min_x
            x2 -= min_x

            p.bugprint(f"Will draw from {x1} {y1} to {x2} {y2}")


            if x2 == x1:
                p.bugprint("horiz")
                y_start, y_end = min([y1, y2]), max([y1, y2])
                for y in range(y_start, y_end+1):                    
                    
                    grid[y][x1] = "#"
                
            elif y2 == y1:
                p.bugprint("vert")
                x_start, x_end = min([x1, x2]), max([x1, x2])
                for  x in range(x_start, x_end+1):
                    
                    grid[y1][x] = "#"

    return grid, max_y


                

                


        


       
       
                
                
                


def display(grid, sands):


    out = ""
    system("cls")
    
    for y, row in enumerate(grid):
        p.bugprint(str(y).zfill(3), end=" ")
        for x, col in enumerate(row):

            for s in sands:
                if s.x == x and s.y == y:

                    out += "O"
                    break
            else:                
                out += col
        out += "\n"

    print(out)
            

            

        
    

    

    

    

        

class Sand:

    def __init__(self, grid):
        self.x = sand_x
        self.y = 0
        self.grid = grid
        self.settled = False

    def fall(self, abyss):

        g = self.grid
        x = self.x
        y = self.y

        if y == len(g) - 1:
            return True

        if g[y+1][x] == ".":
            self.y += 1
        elif g[y+1][x-1] == ".":
            self.y += 1
            self.x -= 1
        elif g[y+1][x+1] == ".":
            self.y += 1
            self.x += 1
        elif g[y+1][x] in "O#":
            self.settled = True


        if self.settled:
            g[self.y][self.x] = "O"


        

def solve(data):
    count = 0


    grid, abyss = create_caves(data)

    grid[0][11] = "+"



    abyss = False

    

    sands = []

    
    
    while not abyss:
        
        sands.append(Sand(grid))
        
        while not sands[-1].settled:    

            abyss_met = sands[-1].fall(abyss)
            display(grid, sands)
            if abyss_met:
                
                return len(sands) - 1

        

        

        

        

        

        

        
    
        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
