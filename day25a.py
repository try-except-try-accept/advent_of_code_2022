from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from itertools import product
from timeit import timeit

PP_ARGS = False, False #rotate, cast int

DAY = 25
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122///2=-1=0"""

DEBUG = True


def calculate_snafu(target, max_=10):

    bits = 0
    while 5 ** bits < target:
        bits += 1

    print("target is", target)
    print(bits, "bits needed")

    input()

    bits -= 1
    
    

    num = [0, 0, 0] + [2 for i in range(bits)]
    dec_num = conv_snafu("2" * bits) + 1
    print("dec num is", dec_num);   input()


    calc_req = target-dec_num
    print("Will need to iterate through", calc_req, "Calculations")


    start = timeit()
    count = 0
    
    while True:
        i = -1
        num[i] += 1

        while num[i] == 3:
            num[i-1] += 1
            num[i] = -2
            i -= 1

        if dec_num == target:
            snafu = "".join({-2:"=", -1:"-", 0:"0", 1:"1", 2:"2"}[v] for v in num)       
            snafu = snafu.lstrip("0")
            return snafu

        dec_num += 1
        count += 1

        if count == 1000000:
            stop = timeit()

            time_diff = stop - start

            print(f"It took {time_diff} to do 1000000 calculations.")
            print(f"It'll take {time_diff * calc_req/1000000} to finish")


def conv_snafu(num):
    this_snafu = 0
    for col, bit in enumerate(reversed(num)):
        col_val = "=-012".index(bit)-2

        this_snafu += col_val * (5 ** col)
    return this_snafu
      


def increment(bits):
    bits[-1] += 1
    

def solve(data):
    total = 0

    for row in data:
            
        total += conv_snafu(row)


    print("Total is", total)

    return calculate_snafu(total)   



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
