from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from numpy import rot90

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

10R5L5R10L4R5L5///5031"""



DEBUG = False


RDLU = ((1, 0),
        (0, 1),
        (-1, 0),
        (0, -1))
        
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

top, back, left, front, bottom, right = 0, 1, 2, 3, 4, 5

FACE_MATRIX = [row.split("\t") for row in '''right	left	front	right	right	top
front	bottom	bottom	bottom	back	back
left	right	back	left	left	bottom
back	top	top	top	front	front'''.splitlines()]


ORIENTATION_MATRIX = [[eval(i) for i in row.split("\t")] for row in '''LEFT	RIGHT	RIGHT	DOWN	RIGHT	LEFT
DOWN	UP	RIGHT	DOWN	UP	RIGHT
DOWN	UP	LEFT	LEFT	UP	LEFT
DOWN	DOWN	RIGHT	UP	UP	LEFT'''.splitlines()]

invert = lambda n, dim : abs(n-(dim-1))

x_and_invert_y =     lambda x, y, dim: (x, invert(y, dim))
x_and_zero =         lambda x, y, dim: (x, 0)
y_and_zero =         lambda x, y, dim: (y, 0)
invert_x_and_zero =  lambda x, y, dim: (invert(x, dim), 0)
invert_y_and_zero =  lambda x, y, dim: (invert(y, dim), 0)

invert_x_and_y =     lambda x, y, dim: (invert(x, dim), y)
invert_y_and_max =   lambda x, y, dim: (invert(y, dim), dim - 1)

zero_and_y =         lambda x, y, dim: (0, y)
zero_and_x =         lambda x, y, dim: (0, x)
zero_and_invert_x =  lambda x, y, dim: (0, invert(x, dim))


max_and_y =          lambda x, y, dim: (dim - 1, y)
max_and_invert_x =   lambda x, y, dim: (dim - 1, invert(x, dim))
max_and_invert_y =   lambda x, y, dim: (dim - 1, invert(y, dim))
x_and_max =          lambda x, y, dim: (x, dim - 1)



                    #top	        back	            left	        front	            bottom	            right
LOCATION_MATRIX = ((max_and_invert_y,	zero_and_y,	    zero_and_y,	        invert_y_and_zero,  zero_and_y,	            x_and_invert_y),            # right
                    (x_and_zero,	invert_x_and_y,	    zero_and_invert_x,	x_and_zero,	    invert_x_and_y,	    zero_and_invert_x),         # down
                    (y_and_zero,	invert_y_and_max,   max_and_y,	        max_and_y,	    invert_y_and_max,       max_and_y),                 # left
                    (invert_x_and_y,	invert_x_and_y,	    zero_and_x,	        x_and_max,	    x_and_max,	            max_and_invert_x))          # up


def rotate(array, rotations=3):
    for _ in range(rotations):
        array = rot90(array)

    return [list(row) for row in array]
    

def move(x, y, dim, num, orientation, current_face, faces):

    

    
    last_face = current_face
    last_actual_x, last_actual_y = x, y
    dir_symbol = ">V<^"[orientation]
    
    
    nx, ny = x, y

    faces[current_face][ny][nx] = dir_symbol

    

    p.bugprint(f"Move {dir_symbol} for {num} steps")

    #display(faces, dim)
    last_orientation = orientation
    

    while num > 0:
        
        
        p.bugprint("last face was", last_face)
        
        vector = RDLU[orientation]
        p.bugprint("was At", nx, ny)
        p.bugprint(f"Orientation is {'>V<^'[orientation]}, current face is {current_face}, vector is {vector}")
        
        

        nx = nx + vector[0]
        ny = ny + vector[1]

        ax, ay = None, None

        if nx < 0:
            ax, ay = 0, ny
        elif ny < 0:
            ax, ay = nx, 0
        elif nx == dim:
            ax, ay = dim-1, ny
        elif ny == dim:
            ax, ay = nx, dim - 1



        if ax is not None or ay is not None:
            fnum = eval(current_face)
        
            current_face = FACE_MATRIX[last_orientation][fnum]

            orientation = ORIENTATION_MATRIX[last_orientation][fnum]

            p.bugprint("Location matrix index at", last_orientation, fnum)
            nx, ny = LOCATION_MATRIX[last_orientation][fnum](ax, ay, dim)

        
        

        if faces[current_face][ny][nx] == "#":         # if hit brick, last pos was final pos
            p.bugprint("Hit brick on", current_face, "at", nx, ny)
            return last_actual_x, last_actual_y, last_orientation, last_face

        else:            
            p.bugprint("No obstacle  on", current_face, "at", nx, ny)
            last_actual_x, last_actual_y = nx, ny
            dir_symbol = ">V<^"[orientation]
            faces[current_face][ny][nx] = dir_symbol
            
            if DEBUG:
                display(faces, dim)
                
            num -= 1
            p.bugprint(num, "steps remain..")
            last_face = current_face
            last_orientation = orientation

            
        
    return last_actual_x, last_actual_y, orientation, current_face

        
        
def display(faces, dim):

    for row in faces["top"]:
        print((dim*2*" ") + "".join(row))


    for one, two, three in zip(faces["back"], faces["left"], faces["front"]):
        print("".join(one+two+three))
    
                
    for one, two in zip(faces["bottom"], faces["right"]):
        
        print((dim*2*" ") + "".join(one+two))
    
    p.buginput()
        
    


def solve(data):
    count = 0


    
    board_map = data[:-2]



    
    board_map = [list(row.strip()) for row in board_map]

    
        
    
    path = list(data[-1])




    if TRANSLATE:
        # puzzle data
        DIM = len(board_map) // 4
        
        line1 = board_map[:DIM]
        line2 = board_map[DIM:DIM*2]
        line3 = board_map[DIM*2:DIM*3]
        line4 = board_map[DIM*3:DIM*4]



        for line in (line1, line2, line3, line4):
            
            print(len(line), len(line[0]))

        faces = {

        'top' : [row[:DIM] for row in line1],
        'back' : rotate([row[:DIM] for row in line4]),
        'left' : rotate([row[:DIM] for row in line3]),
        'front' : [row[:DIM] for row in line2],
        'bottom' : [row[DIM:(DIM*2)] for row in line3],
        'right' : rotate([row[(DIM):DIM*2] for row in line1], 2)

        }


    else:
        # test data cube net
        DIM = len(board_map) // 3

        

        middle_faces = board_map[DIM:(DIM*2)]

        faces = {

        'top' : [row for row in board_map[:DIM]],
        'back' : [row[:DIM] for row in middle_faces],
        'left' : [row[DIM:(DIM*2)] for row in middle_faces],
        'front' : [row[(DIM*2):(DIM*3)] for row in middle_faces],
        'bottom' : [row[:DIM] for row in board_map[(DIM*2):]],
        'right' : [row[DIM:(DIM*2)] for row in board_map[(DIM*2):]]

        }

    for f, data in faces.items():

        print(f, len(data), len(data[0]))
    

    

    orientation = 0

    x, y = 0, 0




    current_face = "top"
    
    num = ""
    dir_symbol = ">"
    while path:
        

        next_char = path.pop(0)

        if next_char in "LR":
            try:
                x, y, orientation, current_face = move(x, y, DIM, int(num), orientation, current_face, faces)
            except Exception as e:
                display(faces, DIM)
                raise e
                
            num = ""
            
            if next_char == "L":
                orientation = ((orientation - 1) % 4)
            else:
                orientation = ((orientation + 1) % 4)

            dir_symbol = ">V<^"[orientation]
            continue

        num += next_char

    if num:
        x, y, orientation, current_face = move(x, y, DIM, int(num), orientation, current_face, faces)
        num = ""


    print("Final x y", x, y, "current face", current_face)

    if not TRANSLATE:
        # test data
        face_adjust = {"top":(DIM*2, 0),
                   "back":(0, DIM),
                   "left":(DIM, DIM),
                   "front":(DIM*2, DIM),
                   "bottom":(DIM*2, DIM*2),
                   "right":(DIM*3, DIM*2)}[current_face]
    else:
        # puzzle input
        face_adjust = {"top":(DIM, 0),
                   "back":(0, DIM*3),
                   "left":(0, DIM*2),
                   "front":(DIM, DIM),
                   "bottom":(DIM, DIM*2),
                   "right":(DIM*3, 0)}[current_face]

    p.bugprint("Face adjust", face_adjust)

    final_row = y + 1 + face_adjust[1]
    final_col = x + 1 + face_adjust[0]

    print("Final row", final_row)
    print("Final col", final_col)
    print("Final facing", orientation)
    
    display(faces, DIM)
    return sum([1000 * final_row, 4 * final_col, orientation])

TRANSLATE = False


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    p.module_tests(locals())
    if p.check(TESTS, solve):
        TRANSLATE = True
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
