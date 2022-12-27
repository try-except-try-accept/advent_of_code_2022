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

DEBUG = False


def calculate_snafu(target, max_=10):

    bits = 0
    while 5 ** bits < target:
        bits += 1

    p.bugprint("target is", target)
    p.bugprint(bits, "bits needed")

    input()

    bits -= 1
    
    # if it uses >=  1.5 x col value it's a 2.


def int_arr_to_snafu(num):
    snafu = "".join({-2:"=", -1:"-", 0:"0", 1:"1", 2:"2"}[v] for v in num)
    return snafu.lstrip("0")

def conv_dec_to_snafu(target):

    yield "0"
    
    num = [0 for i in range(abs(target))]


    if target > 0: # positive mode
        dec_num = 1

        condition = True
        while condition:
            i = -1
            num[i] += 1

            while num[i] == 3:
                num[i-1] += 1

                num[i] = -2

                i -= 1

            yield int_arr_to_snafu(num)

            dec_num += 1
            condition = dec_num < target
        dec_num = 1
        
    else:
        dec_num = -1
        condition = True
        while condition:
            i = -1
            num[i] -= 1

            while num[i] == -3:
                num[i-1] -= 1

                num[i] = 2

                i -= 1

            yield int_arr_to_snafu(num)

            dec_num -= 1
            condition = dec_num > target

    


def conv_snafu_to_dec(num):
    this_snafu = 0
    for col, bit in enumerate(reversed(num)):
        col_val = "=-012".index(bit)-2

        this_snafu += col_val * (5 ** col)
    return this_snafu
      


pos_snafus = list(conv_dec_to_snafu(1000))

neg_snafus = list(conv_dec_to_snafu(-1000))
    

def solve(data):
    total = 0

    longest_snafu = len(max(data, key=len))

    cols = [0 for i in range(longest_snafu)]

    answer = ""

    col_index = -1
    for col in range(longest_snafu):

        p.bugprint("Adding col", col_index)

        calc = " "
        
        for row in data:
            
            try:
                cols[col_index] += conv_snafu_to_dec(row[col_index])
                p.bugprint("+" + row.rjust(10, " "))
                calc += " + " + row[col_index]
            except IndexError:
                continue

        
        col_sum = cols[col_index]
        p.bugprint(f"{calc} = {col_sum}")

        if col_sum >= 0:
            result = pos_snafus[col_sum]
        else:
            result = neg_snafus[abs(col_sum)]

        p.bugprint(f"Which is {result} in snafu")

        answer = result[-1] + answer

        p.bugprint(f"Answer is now {answer}")

        carry = result[:-1]

        p.bugprint("And carry the", carry)

        data.append(carry + ("0" * abs(col_index)))

        col_index -= 1

        
    answer = carry + answer
        
    p.bugprint(answer)
 

    return answer



if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))



