from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import ceil
from timeit import timeit


PP_ARGS = False, False #rotate, cast int

DAY = 17
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>///1514285714288"""
MOVE_LIMIT = 1000000000000

WIDTH = 7
DEBUG = False

def init_block_q():
                  ##0123456789ABCDEFGHIJKLMNOPQR
    return [(1,0b011110),                          # flat line
           (3, 0b000100000111000001000),           # cross
           (3, 0b000010000001000011100),           # L shape
           (4, 0b0010000001000000100000010000),    # vert line
           (2, 0b00110000011000)]                  # square

block_q = []

MASK = 0b1111111

LEFT_MASK =  0b1000000100000010000001000000
RIGHT_MASK = 0b0000001000000100000010000001

def isolate_lines(block=0, line=0, num_lines=1, block_height=0):
    """Extract a single line from a block"""

    shift = max(0, block_height - (line + num_lines))
    block = block >> shift * WIDTH

    mask = ((MASK+1) ** num_lines) - 1

    return block & mask

  

def determine_bounds(block=0, fall_point=0, rested=0, block_height=0, num_rows_rested=0):

    """Determines the current bounds based on already rested blocks
and the fall point of the current block"""

    if fall_point <= 0:
        return None
    else:
        # get the rested from the fall point up to the fall point + the length of the block
        line_start = 0 # isolate lines from 0, unless fall point has exceeded top line
        if fall_point > block_height:
            line_start =  fall_point - block_height
        return isolate_lines(rested, line_start, min(fall_point, block_height), num_rows_rested)

def display_interim(block):
    if DEBUG:
        debinarise(block)        

def check_if_cant_move(fall_point, bounds, block):
    left = block << 1 & bounds == 0
    right = block >> 1 & bounds == 0
    return not (left or right)
    
def process_jet_stream(bounds=0, block=0, jet=None):
    """Accepts a current block and one or more jet instructions, and
    bounds according to rested blocks and fall point"""
    jet = list(jet)

    while jet:
        didnt_move = False

        this_jet = jet.pop(0)
        # if already on edge, just skip
        if this_jet == "<":
            p.bugprint("Jet of gas pushes rock left", end="")
            if block & LEFT_MASK != 0:
                p.bugprint(", but nothing happens as hit left wall")
                display_interim(block)
                didnt_move = True
                continue
        elif this_jet == ">":
            p.bugprint("Jet of gas pushes rock right", end="")
            if block & RIGHT_MASK != 0:
                p.bugprint(", but nothing happens as hit right wall")
                display_interim(block)
                didnt_move = True
                continue
        p.bugprint()
        

        
        old_block = block
        #p.bugprint("Block was", bin(block))
        block = eval(f"{block} {this_jet*2} 1")
        
        #p.bugprint("Block now", bin(block))
        if bounds:
                
            # check against landed blocks
            if block & bounds != 0:
                p.bugprint(", but nothing happens as hit rested")
                block = old_block
                didnt_move = True
        display_interim(block)

    return block, didnt_move

    
def rest_blocks(rested=0, block=0, fall_point=0, num_rows_rested=0, block_height=0):
    """Amalgamate already rested blocks with newly resting block
at a given fall point"""


    if num_rows_rested == 0:
        return block, block_height, block_height
    shift_needed = num_rows_rested - fall_point
    

    block = block << (WIDTH * shift_needed)

    if rested & block != 0:
        raise Exception("merge error - trying to merge overlapping blocks")


    # cannot decrease

    newly_rested = max(0, (block_height - fall_point))
    
    num_now_rested = num_rows_rested +  newly_rested
    
    rested = (rested | block) # >> (WIDTH * shift_needed)   # why need to shift back?

    truncate = 0


    for line in range(fall_point - block_height, fall_point + 1 + newly_rested):

        if isolate_lines(block=rested, line=line, num_lines=1, block_height=num_now_rested) ^ MASK == 0: # full row found

            truncate = num_now_rested - line
            break


    if truncate:

        rested = rested >> (WIDTH * truncate)
        num_now_rested = (num_rows_rested - truncate) + newly_rested




    return rested, num_now_rested, newly_rested

def check_if_cant_fall(fall_point=0, rested=0, block=0, num_rows_rested=0):
    """Return true if rested blocks below prevent current block from falling further"""
    # shift block to correlate with correct row of rested
    
    # if AND result is not 0, return True

    if fall_point == num_rows_rested:
        return True


    shift_req = max(0, (num_rows_rested - fall_point)-1)


    block = block << (WIDTH * shift_req)

    if block & rested != 0:
        return True

    return False
    
    
def get_jets(num, jet_q):

    for i in range(num):
        jet = jet_q.pop(0)        
        jet_q.append(jet)
        yield jet


def count_sub_sequence(rested_record, pattern_check, length):

    if len(rested_record) < length + 1: return None

    result = rested_record[:length] == pattern_check == rested_record[-length:]
    for i in range(0, len(rested_record)-length):
        if rested_record[i:i+length] == pattern_check:
            return i

    return None

    


def solve(data):
    global DEBUG

    SUB_PATTERN_LENGTH = 100
  

    block_q = init_block_q()

    jet_q = list(data[0])

    rested = 0

    bounds = 0
    num_rows_rested = 0
    overall_rested = 0

    rested_combinations = set()

    start = timeit()

    pattern_check = []
    rested_record = []

    newly_rested_record = []
    

    for turn in range(MOVE_LIMIT):
        
        newly_rested = 0
        
        sequence_start = count_sub_sequence(rested_record, pattern_check, SUB_PATTERN_LENGTH)

        if sequence_start is not None:
            print("Repetition found.")
            
            
            rested_record = rested_record[:-SUB_PATTERN_LENGTH]
            
            sequence_length = len(rested_record) - sequence_start

            print("Record of ", len(newly_rested_record), "newly rested counts")
            print("Record of ", len(rested_record), "rested block formations")

            rested_during_sequence = newly_rested_record[sequence_start:-SUB_PATTERN_LENGTH]

            total_rested_during_sequence = sum(rested_during_sequence)

            print("sequence_start", sequence_start, "length", sequence_length)

            num_more_sequences = (MOVE_LIMIT-(turn-SUB_PATTERN_LENGTH)) / sequence_length

            num_more_whole_seq = int(num_more_sequences)

            fraction_of_seq = num_more_sequences - num_more_whole_seq

            print("Sequence will repeat for", num_more_whole_seq, "more times")

            print("Rows rested during sequence", rested_during_sequence)

            rested_by_first_seq = sum(newly_rested_record[:-SUB_PATTERN_LENGTH])

            print("Rows rested by time first sequence has completed", rested_by_first_seq)

            final_row_count = int(rested_by_first_seq + (total_rested_during_sequence * num_more_whole_seq))

            print("Rows rested after all sequences have completed", final_row_count)

            print("With", fraction_of_seq, "fraction of a sequence to still sort out...")

            rested_during_fraction_of_a_seq = sum(rested_during_sequence[:int(len(rested_during_sequence) * fraction_of_seq)])


            return final_row_count + rested_during_fraction_of_a_seq
            
        

        p.bugprint("A new block begins to fall")
        bounds = 0

        # get next block
        block = block_q.pop(0)
        block_q.append(block)
        block_height, block = block
        
        # can always fall at least 3 spaces


        jet = get_jets(3, jet_q)
        
        fall_point = 0


        block, _ = process_jet_stream(bounds, block, jet)

        couldnt_fall = check_if_cant_fall(fall_point, rested, block, num_rows_rested)

        landed = False
        while not landed:
            
            jet = get_jets(1, jet_q)
            
            block, didnt_move = process_jet_stream(bounds, block, jet)
            bounds = determine_bounds(block, fall_point, rested, block_height, num_rows_rested)

            #debinarise(block)
            #debinarise(rested)
            p.bugprint("Rock falls 1 unit")

            
            cant_fall = check_if_cant_fall(fall_point, rested, block, num_rows_rested)
            if not cant_fall:
                fall_point += 1
               
                bounds = determine_bounds(block, fall_point, rested, block_height, num_rows_rested)

            if cant_fall:

                p.bugprint("Block came to rest")
                landed = True
                
                rested, num_rows_rested, newly_rested = rest_blocks(fall_point=fall_point, rested=rested,
                                                      block=block, num_rows_rested=num_rows_rested,
                                                      block_height=block_height)

                overall_rested += newly_rested

                #debinarise(rested)

                newly_rested_record.append(newly_rested)

                
                
                top_row = isolate_lines(block=rested, line=0, num_lines=1, block_height=num_rows_rested)

                rested_record.append(top_row)
                pattern_check.append(top_row)
                
                if len(pattern_check) == SUB_PATTERN_LENGTH + 1:
                    pattern_check.pop(0)


        


    return overall_rested
        
def debinarise(num):
    if type(num) == tuple:  num = num[0]
    try:
        
        num = bin(num)[2:]
        p.bugprint(len(num))
        fill_row = WIDTH * ceil(len(num) / WIDTH)
        p.bugprint("Will z fill", fill_row)
        num = num.zfill(fill_row)

        for i in range(0, len(num), WIDTH):
            p.bugprint(num[i:i+WIDTH].replace("0", ".").replace("1", "█"))
        
    except Exception as e:
        p.bugprint(e)
        p.bugprint(f"Problem debinarising {num}")


def convert_arg(data):
    if set(data) == set(["█", "."]):
        data = data.replace(".", "0").replace("█", "1")
        data = int(data, 2)

    try:
        return int(data)                              # return integer value
    except ValueError:
        if data in "TrueFalseNone": return eval(data) # return bool/null flag
        return data                                   # return > / < string
    
def process_test_args(data):

    data = tuple(map(convert_arg, data.split(",")))

    if len(data) == 1:  data = data[0]

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
                
                data = {arg:process_test_args(value) for arg, value in data.items()}
                expected = data.pop("result")

                p.bugprint(data)

                actual = eval(f"{func}(**data)")
     
                if expected != actual:
                    p.bugprint(this_test)
                    p.bugprint(f"RECEIVED: {actual}\n EXPECTED {expected}")
                    p.bugprint(f"received")
                    debinarise(actual)
                    raise Exception(f"Test number {test_num} failed\n{e}")
                p.bugprint(f"Test number {test_num} ({func}) PASSED 🎉")
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
    if input("Run module tests?"):
        module_tests()
        input("all module tests passed")

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
