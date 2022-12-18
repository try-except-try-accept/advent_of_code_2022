from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

import tetris

PP_ARGS = False, False #rotate, cast int

DAY = 17
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>///3068"""
MOVE_LIMIT = 2022

WIDTH = 7
DEBUG = False

##block_q = [[0b011110],                                      # flat line
##           [0b0001000, 0b0011100, 0b0001000],               # cross
##           [0b0000100, 0b0000100, 0b0011100],               # L shape
##           [0b0010000, 0b0010000, 0b0010000, 0b0010000],    # vert line
##           [0b0011000, 0b0011000]]                          # square

            ##0123456789ABCDEFGHIJKLMNOPQR
block_q = [0b011110,                          # flat line
           0b000100000111000001000,           # cross
           0b000010000001000011100,           # L shape
           0b0010000001000000100000010000,    # vert line
           0b00110000011000]                  # square


MASK = 0b1111111

LEFT_MASK =  0b1000000100000010000001000000
RIGHT_MASK = 0b0000001000000100000010000001

def isolate_lines(block=0, line=0, num_lines=1):
    """Extract a single line from a block"""
    rows = get_block_length(block)


    shift = rows - (line + num_lines)
    #p.bugprint("Shift is", shift, "bc", rows, "rows and", line, "line")

    length = 7 * 5

    #p.bugprint(f"Block is {bin(block): >70} ".center(length))
    block = block >> shift * WIDTH

    mask = ((MASK+1) ** num_lines) - 1

    #p.bugprint(f"Mask is  {bin(mask): >70}".center(length))

    return block & mask

  

def get_block_length(block):
    """Determine how many rows a binary block takes up"""
    poss_length = 0
    while True:
        if block < 2 ** (WIDTH * poss_length):
            #p.bugprint("This block has length", poss_length)
            return poss_length
        poss_length += 1

def determine_bounds(block=0, fall_point=0, rested=0):

    """Determines the current bounds based on already rested blocks
and the fall point of the current block"""
    block_length = get_block_length(block)
    if fall_point <= 0:
        return None
    else:
        # get the rested from the fall point up to the fall point + the length of the block
        line_start = 0 # isolate lines from 0, unless fall point has exceeded top line
        if fall_point > block_length:
            line_start =  fall_point - block_length
        return isolate_lines(rested, line_start, min(fall_point, block_length))


def process_jet_stream(bounds=0, block=0, jet=None):
    """Accepts a current block and one or more jet instructions, and
    bounds according to rested blocks and fall point"""
    jet = list(jet)
    p.bugprint("Got bounds its", bounds)
    p.bugprint("Got block its", block)
    

    while jet:

        this_jet = jet.pop(0)
        # if already on edge, just skip
        if this_jet == "<":
            p.bugprint("Jet of gas pushes rock left", end="")
            if block & LEFT_MASK != 0:
                p.bugprint(", but nothing happens.")
                continue
        elif this_jet == ">":
            p.bugprint("Jet of gas pushes rock right", end="")
            if block & RIGHT_MASK != 0:
                p.bugprint(", but nothing happens.")
                continue
        p.bugprint()

        
        old_block = block
        #p.bugprint("Block was", bin(block))
        block = eval(f"{block} {this_jet*2} 1")
        #p.bugprint("Block now", bin(block))
        if bounds:
                
            # check against landed blocks
            if block & bounds != 0:
                #p.bugprint(", but nothing happens.")
                block = old_block

    return block

    
def rest_blocks(rested=0, block=0, fall_point=0):
    """Amalgamate already rested blocks with newly resting block
at a given fall point"""
    rows_rested = get_block_length(rested)

    if rows_rested == 0:
        return block

    shift_needed = rows_rested - fall_point

    block = block << (WIDTH * shift_needed)

    if rested & block != 0:
        raise Exception("merge error - trying to merge overlapping blocks")

    shift = 0

## this is cruddy
##    for i in range(rows_rested-1): 
##        this_line = isolate_lines(rested, i, 1)
##        next_line = isolate_lines(rested, i+1, 1)
##        if this_line | next_line == MASK:
##            print("Found truncation point...")
##            shift = i
##            break

    return (rested | block) >> (WIDTH * shift)


def check_if_cant_fall(fall_point=0, rested=0, block=0):
    """Return true if rested blocks below prevent current block from falling further"""
    # shift block to correlate with correct row of rested
    
    # if AND result is not 0, return True

    rows_rested = get_block_length(rested)

    if fall_point == rows_rested:
        return True


    shift_req = rows_rested - fall_point - 1

    block = block << (WIDTH * shift_req)

    if block & rested != 0:
        return True

    return False
    
    


def solve(data):

  

    

    jet_q = list(data[0])

    rested = 0

    bounds = 0
  


    for turn in range(MOVE_LIMIT):
        print("turn", turn)

        # get next block
        block = block_q.pop(0)
        block_q.append(block)
        
        # can always fall at least 3 spaces
        next_3_jets = jet_q[:3]
        jet_q += list(next_3_jets)

        fall_point = 0

        block = process_jet_stream(bounds, block, next_3_jets)

        couldnt_fall = check_if_cant_fall(fall_point, rested, block)

        
        landed = False
        while not landed:

            jet = jet_q[:3]
            jet_q += [jet]


            block = process_jet_stream(bounds, block, jet)
            
            cant_fall = check_if_cant_fall(fall_point, rested, block)

            if not cant_fall:       # can fall
                fall_point += 1
                bounds = determine_bounds(block, fall_point, rested)
            elif couldnt_fall:      # can't fall, and couldn't fall last time
                p.bugprint("Block came to rest")
                landed = True
                
                rested = rest_blocks(fall_point=fall_point, rested=rested, block=block)

            couldnt_fall = cant_fall

            
    return get_block_length(rested)      
        
def debinarise(num):
    try:

        num = bin(num)[2:]

        for i in range(0, len(num), WIDTH):
            p.bugprint(num[i:i+WIDTH+1].replace("0", ".").replace("1", "█"))
        
    except:
        p.bugprint(f"Problem debinarising {num}")
        
    
def binarise(data):
    if set(data) == set(["█", "."]):

        data = data.replace(".", "0").replace("█", "1")
        return int(data, 2)


    try:
        return int(data)
    except ValueError:
        if data in "TrueFalseNone": return eval(data)
        return data
               
def module_tests():
    with open("day17.tests", encoding="utf-8") as f:
        test_data = f.read()

    test_num = 1
    func = None
    data = {}
    this_test = ""

    p.bugprint(f"processing {test_data.count('test:')}")
    for line in test_data.splitlines():

        

        if "test:" in line:
            p.bugprint(line)
            e = None
            if func:
                
                data = {arg:binarise(value) for arg, value in data.items()}
                expected = data.pop("result")

                actual = eval(f"{func}(**data)")
     
                if expected != actual:
                    p.bugprint(this_test)
                    p.bugprint(f"RECEIVED: {actual}\n EXPECTED {expected}")
                    p.bugprint(f"received")
                    debinarise(actual)
                    raise Exception(f"Test number {test_num} failed\n{e}")
                p.bugprint(f"Test number {test_num} PASSED 🎉")
                test_num += 1

                p.bugprint()
                
                
            func = line.split("test:")[1]
            data = {}
            this_test = line + "\n"

        else:
            if ":" in line:
                line_split = line.split(":")
                this_arg = line_split[0]
                if len(line) > 1:
                    data[this_arg] = line_split[1] # test value on same line
            else:
                data[this_arg] += line

            this_test += line + "\n"


           
                

        


            

            

                
                
                
        




if __name__ == "__main__":
    
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    module_tests()

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
