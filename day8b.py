from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import prod
from random import randint
PP_ARGS = False, False #rotate, cast int


DAY = 8
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """30373
25512
65332
33549
35390///8
---111111789
111111145
111111111
987654311
111111111///21"""



DEBUG = False

def display(data, visible):
    if not DEBUG:   return
    s = ""
    for y in range(len(data)):
        for x in range(len(data[y])):
            tree = data[y][x]
            s += str(tree)

        s += "\n"
    print(s)

    


def get_line_of_sight(x, y, data, w, h):

    if x == 0 or x == w - 1 or y == 0 or y == h - 1:
        return 0

    viewpoint = data[y][x]

    p.bugprint("line of sight from", x, y)


    scenery = [0, 0, 0, 0]

    display(data, [])

    directions = "up,left,down,right".split(",")


    if y == 3 and x == 2:
        print(x, y)
    


    for dim_index, bound, mov_change, scen_index in zip((1, 0, 1, 0),
                                                        (h, w, h, w),
                                                         (-1, -1, 1, 1),
                                                         (0, 1, 2, 3)):

        mov = [x, y]
        biggest = 0
        comp_tree = None
        p.bugprint(f"looking {directions[scen_index]}")
        while mov[dim_index] > 0 and mov[dim_index] < bound-1:
            mov[dim_index] += mov_change
            comp_tree = data[mov[1]][mov[0]]
            #p.bugprint(mov)
            
            if comp_tree >= biggest or (comp_tree < viewpoint and viewpoint > biggest):
                scenery[scen_index] += 1
                biggest = comp_tree

                p.bugprint(f"can see", comp_tree)
            else:
                p.bugprint(f"can't see", comp_tree)

            if comp_tree >= viewpoint:
                break
 

    p.bugprint(scenery)
    answer =  prod(scenery)
    if answer == 8:
        p.buginput()

    return answer
        


def solve(data):
    count = 0
   
    W = len(data[0])
    H = len(data)

    data = [list(map(int, d)) for d in data]

    best_los = 0
    
    for y in range(H):
        for x in range(W):


         
            los = get_line_of_sight(x, y, data, W, H)
            p.bugprint(los)

            

            

            if los > best_los:
                best_los = los

    return best_los




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
