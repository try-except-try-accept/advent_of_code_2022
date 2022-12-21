from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 21
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32///152"""

DEBUG = False


def rpn_eval(exp):
    stack = []
    for token in exp.split():
        if token.replace("-", "").isdigit():
            stack.append(int(token))
        else:
            stack.append(eval(f"{stack.pop(-2)} {token} {stack.pop(-1)}"))

    if len(stack) > 1:
        raise Exception("Unexhausted stack error")
    else:
        return int(stack[0])

def rpn_convert(exp):
    if exp.replace("-", "").isdigit():  return int(exp)

    tokens = exp.split()
    tokens.append(tokens.pop(1))
    return " ".join(tokens)
        


def solve(data):

    def try_eval(exp):

        try:
            return rpn_eval(exp)
        except Exception as e:
            return exp

    def prep(exp):

        return try_eval(rpn_convert(exp))
  
            
    count = 0

    jobs = {}

    [jobs.update({row.split(": ")[0]:prep(row.split(": ")[1])}) for row in data]

    
    to_resolve = 1
    while to_resolve:

        to_resolve = {m:j for m,j in jobs.items() if type(j)==str}

        print(f"{len(to_resolve)} to resolve")
        input()

        for monkey, job in jobs.items():

                if type(job) != str:    continue

                terms = findall("[a-z]{4}", job)

                for t in terms:
                    job = str(job.replace(t, str(try_eval(jobs[t]))))
                
                jobs[monkey] = try_eval(job)
 
        
    

    return int(jobs["root"])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
