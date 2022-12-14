from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from copy import deepcopy

PP_ARGS = False, False #rotate, cast int

DAY = 13
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]///140
"""

DEBUG = False

def compare(left_item, right_item):  
    
    if left_item < right_item:
        p.bugprint("Left side is smaller, so inputs are in the right order")
        return True
    elif right_item < left_item:
        
        p.bugprint("Right side is smaller, so inputs are not in the right order")
        return False
    else:
        return None

  


def walk(left, right, d=0):

    p.bugprint(" "*d, f" - Compare {left} vs. {right}")

    while left:

        left_item = left.pop(0)
        try:
            right_item = right.pop(0)
        except:
            p.bugprint("Right side ran out of items, so inputs are not in the right order")
            return False

        if type(left_item) == list or type(right_item) == list:
            if type(right_item) != list:
                p.bugprint("Mixed types")
                right_item = [right_item]

            if type(left_item) != list:
                p.bugprint("Mixed types")
                left_item = [left_item]

            result = walk(left_item, right_item, d+1)

            if result is not None:
                return result
        else:
            p.bugprint(" "*(d+1), f" - Compare {left_item} vs. {right_item}")

        result = compare(left_item, right_item)

        if result is not None:
            return result

    if len(right):
        p.bugprint("Left side ran out of items, so inputs are in the right order")
        return True
    



 

        

    

    


def solve(data):
    count = 0



    

    data += ["[[2]]", "[[6]]"]


    new = []

    data = [eval(d) for d in data if len(d)]


    print(data)
    
    swapped = True
    pass_num = 1
    while swapped:
        swapped = False

        for i in range(len(data)-pass_num):

            left = data[i]
            right = data[i+1]

            if not walk(deepcopy(left), deepcopy(right)):
                data[i], data[i+1] = right, left
                swapped = True

        pass_num += 1
        
    print("sorted")
    for row in data:
        print(row)
    
    return (data.index([[2]]) + 1) * (data.index([[6]]) + 1)




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
[
