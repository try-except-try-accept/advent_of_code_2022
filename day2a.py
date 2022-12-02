from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 2
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """A Y
B X
C Z///15"""



DEBUG = True


def solve(data):

    
    me =  "XYZ"
    you = "CAB"
    OPTIONS = 3   

    total = 0
    for row in data:        
        you_code, me_code = row.split()

        my_choice = me.index(me_code)
        your_choice = you.index(you_code)      

        total += me.index(me_code) + 1
        
        if my_choice == your_choice:            
            total += 6  # i won            
        elif my_choice == (your_choice + 1) % OPTIONS:
            pass # i lost            
        else:
            total += 3  # it was a draw        
    
    return total
            

        

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
