from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 18
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1,1,1
2,1,1///10
---2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5///64"""

DEBUG = False


##from turtle import Turtle
##t = Turtle()

CUBE_SIZE = 100

def cube(x, y, z):

    x *= CUBE_SIZE
    y *= CUBE_SIZE
##    
##
##    x = x / z
##    y = y / z

    t.penup()
    t.goto(x, y)
    t.pendown()

    cube_size = CUBE_SIZE

    half_cube = cube_size // 2

        
    # forming front square face
    for i in range(4):
        t.forward(cube_size)
        t.left(90)
      
    # bottom left side
    t.goto(x+half_cube,y+half_cube)
      
    # forming back square face
    for i in range(4):
        t.forward(cube_size)
        t.left(90)
      
    # bottom right side
    t.goto(x+cube_size+half_cube,y+half_cube)
    t.goto(x+cube_size,y)
      
    # top right side
    t.goto(x+cube_size,y+cube_size)
    t.goto(x+cube_size+half_cube,y+cube_size+half_cube)
      
    # top left side
    t.goto(x+half_cube,y+cube_size+half_cube)
    t.goto(x,y+cube_size)


def solve(data):

    
    def check_cube(check, cube):
        p.bugprint(check, "is connected to", end="")
        for axis,i,j,k in (('z', 0, 1, 2),
                           ('x', 1, 2, 0),
                           ('y', 2, 0, 1)):
            if (check[i], check[j]) == (cube[i], cube[j]):
                if (cube[k]-check[k]) == 1:
                    p.bugprint(cube, "on", axis, "axis")
                    return axis
                elif (cube[k]-check[k]) == -1:
                    p.bugprint(cube, "on -", axis, "axis")
                    return "-"+axis

        p.bugprint(" nuffing")
        
    unconnected = 0

    cubes = [tuple(map(int, row.split(","))) for row in data]

    for check in cubes:
        #cube(*check)
        connected = set(check_cube(check, cube) for cube in cubes)
        connected.remove(None)

        unconnected += (6 - len(connected))    

    return unconnected




if __name__ == "__main__":

    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
