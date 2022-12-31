from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

class InvalidPocketException(Exception):
    pass

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
2,3,5///58"""

DEBUG = False

def explore(x, y, z, this_pocket, cubes, pockets, bounds):
    """Explore surrounding cubes to determine size of pocket
    raise error if water reached or pocket already explored"""
    if (x, y, z) in pockets or x < bounds[0] or x > bounds[3] or \
                               y < bounds[1] or y > bounds[4] or \
                               z < bounds[2] or z > bounds[5]:
        raise InvalidPocketException
    
    if (x, y, z) in (cubes | this_pocket):
        return
    
    this_pocket.add((x, y, z))

    for xc, yc, zc in ((1,0,0),
                       (-1,0,0),
                       (0,1,0),
                       (0,-1,0),
                       (0,0,-1),
                       (0,0,1)):

        explore(x+xc, y+yc, z+zc, this_pocket, cubes, pockets, bounds)
   

def check_cube(check, cube):
    """Determine if cube is connected to another cube"""
    
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


def calculate_surface(cubes):
    """Calculate surface area of a set of cubes"""
    
    surface = 0

    for check in cubes:
        connected = set(check_cube(check, cube) for cube in cubes)
        connected.remove(None)
        surface += (6 - len(connected))

    return surface



def solve(data):


    cubes = set([tuple(map(int, row.split(","))) for row in data])


    overall_surface = calculate_surface(cubes)


    x_min = min(cubes)[0]
    x_max = max(cubes)[0]
    y_min = min(cubes, key=lambda y: y[1])[1]
    y_max = max(cubes, key=lambda y: y[1])[1]
    z_min = min(cubes, key=lambda z: z[2])[2]
    z_max = max(cubes, key=lambda z: z[2])[2]
    
    bounds = (x_min, y_min, z_min, x_max, y_max, z_max)

    pockets = set()
    
    for z in range(z_min+1, z_max):
        for y in range(y_min+1, y_max):
            for x in range(x_min+1, x_max):
                check = (x, y, z)
                if check in (cubes):  continue
                this_pocket = set()
                try:
                    explore(x, y, z, this_pocket, cubes, pockets, bounds)
                    
                except InvalidPocketException:
                    continue
                
                pockets |= this_pocket

    return overall_surface - calculate_surface(pockets)


if __name__ == "__main__":

    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))

