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

10R5L5R10L4R5L5///5031"""

TESTS = """    ..
    ..
......
......
    ....
    ....

1L10R///1000"""

DEBUG = True


RDLU = ((1, 0),
        (0, 1),
        (-1, 0),
        (0, -1))
        


def move(x, y, dim, num, orientation, current_face, faces):

    print(faces)

    input()
    last_actual_x, last_actual_y = x, y

    

    last_actual_x, last_actual_y = x, y
    dir_symbol = ">V<^"[orientation]
    
    
    nx, ny = x, y

    faces[current_face][ny][nx] = dir_symbol

    

    p.bugprint(f"Move {dir_symbol} for {num} steps")

    #display(faces, dim)

    

    while num > 0:
        
        
        vector = RDLU[orientation]
        print("was At", nx, ny)
        p.bugprint(f"Orientation is {'>V<^'[orientation]}, current face is {current_face}, vector is {vector}")
        
        

        nx = nx + vector[0]
        ny = ny + vector[1]

        print("now At", nx, ny)

        new_orientation = None

        
        
        if ny < 0:              # off top of face
            new_orientation = {"left":0, "back":1, "right":2, "top":1}.get(current_face)
            current_face = {"top":"back", "bottom":"front", "front":"top", "left":"top", "back":"bottom", "right":"top"}[current_face]
            
        elif ny > dim-1:
            p.bugprint(" off bottom of face")
            new_orientation = {"left":0, "bottom":3, "right":0}.get(current_face)
            current_face = {"top":"front", "bottom":"back", "front":"bottom", "left":"bottom", "back":"bottom", "right":"bottom"}[current_face]          

        elif nx < 0:            # off left of face
            new_orientation = {"top":1, "bottom":3, "back":3}.get(current_face)
            current_face = {"top":"left", "bottom":"left", "front":"left", "left":"back", "back":"right", "right":"bottom"}[current_face]

        elif nx > dim-1:          # off right of face
            p.bugprint("Went off right")
            new_orientation = {"front":1, "top":2, "right":2}.get(current_face)
            current_face = {"top":"right", "bottom":"right", "front":"right", "left":"front", "back":"left", "right":"top"}[current_face]

        if new_orientation is None: new_orientation = orientation
        orientation_change = new_orientation - orientation

        if orientation_change == 0:
            ny %= dim
            nx %= dim

        elif orientation_change == 1:
            print("orientation change 1", new_orientation-orientation)

            nx = (dim-1) - ny
            ny = dim-1            
            orientation = new_orientation

        elif orientation_change == 3:
            print("orientation change 3", orientation_change)
            ny = nx
            orientation = new_orientation
            nx = dim-1
        elif orientation_change == -3:
            print("orientation change 3", orientation_change)
            ny = 0
            orientation = new_orientation
            

        elif orientation_change == 2:
            print("orientation change 2", orientation_change)
            nx = (dim-1) - nx
            ny = ny - 1     
            orientation = new_orientation

        elif orientation_change == -2:
            print("orientation change 2", orientation_change)
            nx = (dim-1) - nx
            ny = ny + 1
                
            orientation = new_orientation

        print("Now at", nx, ny)
       

        if faces[current_face][ny][nx] == "#":         # if hit brick, last pos was final pos
            return last_actual_x, last_actual_y, last_orientation, last_face

        else:                                # else hit free space ., counts as a move
            
            last_actual_x, last_actual_y = nx, ny
            dir_symbol = ">V<^"[orientation]
            faces[current_face][ny][nx] = dir_symbol
            
            display(faces, dim)
            num -= 1
            p.bugprint(num, "steps remain..")
            last_face = current_face
            last_orientation = orientation
            
            
        
    return last_actual_x, last_actual_y, orientation, current_face

        
        
def display(faces, dim):

    for row in faces["top"]:
        p.bugprint((dim*2*" ") + "".join(row))


    for one, two, three in zip(faces["back"], faces["left"], faces["front"]):
        p.bugprint("".join(one+two+three))
    
                
    for one, two in zip(faces["bottom"], faces["right"]):
        
        p.bugprint((dim*2*" ") + "".join(one+two))
    
    #input()
        
    


def solve(data):
    count = 0


    
    board_map = data[:-2]
    board_map = [list(row.strip()) for row in board_map]
    
    path = list(data[-1])


    
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

    p.bugprint(faces["bottom"]); input()
    

    orientation = 0

    x, y = 0, 0




    current_face = "top"
    
    num = ""
    dir_symbol = ">"
    while path:
        

        next_char = path.pop(0)

        if next_char in "LR":

            x, y, orientation, current_face = move(x, y, DIM, int(num), orientation, current_face, faces)
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


    face_adjust = {"top":(DIM*2, 0),
                   "back":(0, DIM),
                   "left":(DIM, DIM),
                   "front":(DIM*2, DIM),
                   "bottom":(DIM*2, DIM*2),
                   "right":(DIM*3, DIM*2)}[current_face]

    p.bugprint("Face adjust", face_adjust)

    final_row = y + 1 + face_adjust[1]
    final_col = x + 1 + face_adjust[0]

    print("Final row", final_row)
    print("Final col", final_col)
    
    
    return sum([1000 * final_row, 4 * final_col, orientation])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    p.module_tests(locals())
    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
