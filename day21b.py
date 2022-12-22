from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 21
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """root: pppw == sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: x
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32///301"""

DEBUG = True

def valid_number(token, allow_x=True):
    
    return token.replace("-", "").replace(".", "").isdigit() or allow_x and token == "x"

def rpn_eval(exp, evaluate=True):


    stack = []
    for token in exp.split():
        #print("evaluate=False stack", stack)
        if valid_number(token):
            stack.append(token)
        else:
            new_exp = f"({stack.pop(-2)} {token} {stack.pop(-1)})"
            if evaluate:
                new_exp = eval(new_exp)
            stack.append(new_exp)
    
    if len(stack) > 1:
        print(stack)
        raise Exception("Unexhausted stack error")
    else:
        
        result = stack[0]
        if result == "True":    return bool(1)
        else:
            if evaluate: result = int(result)
            return result

def rpn_convert(exp):
    if exp.replace("-", "").isdigit():  return int(exp)

    if exp == "x":  return exp

    tokens = exp.split()
    tokens.append(tokens.pop(1))
    return " ".join(tokens)
        
def infix_convert(exp):
    return rpn_eval(exp, evaluate=False)


def simplify(exp):

    sub_exps = [None]

    while len(sub_exps):
        sub_exps = []
        for op in "/+-*":
            # what on earth is this

            int_op_ints = "\d{1,10}\s\\" + op + "\s\d{1,10}"
            bracketed_ints = "\(\d{1,10}\)"
            bracketed_reals = "\(\d{1,10}\s\.\d+\)"
            real_op_real = "\d{1,10}\s\.\d+\\" + op + "\d{1,10}\s\.\d+"
            int_op_real = "\d{1,10}\s\\" + op + "\d{1,10}\s\.\d+"
            real_op_int = "\d{1,10}\s\.\d+\\" + op + "\s\d{1,10}"
            

            [sub_exps.extend(findall(patt, exp)) for patt in (int_op_ints,
                                                             bracketed_ints,
                                                             bracketed_reals,
                                                             real_op_real,
                                                             int_op_real,
                                                             real_op_int)]
        for sub in sub_exps:
            print("Found a sub", sub)
            
            exp = exp.replace(sub, str(eval(sub)))


        print("Exp now", exp)
      
    
    return exp

def solve_rpn_simultaneous(exp):
    print(exp)
    stack = []
    inverse = {'+':'-',
               '-':'+',
               '*':'/',
               '/':'*',
               '==':'=='}

    exp = exp.split()

    left_hand_op = None

    stack = []



    
    stack = []

    p.bugprint("rhop", exp)

    op_q = []

    
    exp = infix_convert(" ".join(exp))
    


    p.bugprint("Back to infix...")
    p.bugprint(exp)

    if exp[0] == "(" and exp[-1] == ")":
        exp = exp[1:-1]


    split_exp = exp.split("==")

    lhop, exp = sorted(split_exp, key=len)

    lhop = eval(lhop)
    print(lhop, "is the lhop")
    input()

    exp = exp.strip()

    
    


    while exp != "x":
        exp = simplify(exp)
        print("Expression is now", exp)
        print("Lhop is now", lhop)
        input()


        # this is causing the problem

        # create detect_redundant_brackets() function... 
        if exp[0] == "(" and exp[-1] == ")":
            print("Remove braks")
            exp = exp[1:-1]
            continue

        split_exp = exp.split()

        
        if valid_number(split_exp[-1] , allow_x=False):
            num = split_exp[-1]
            op = split_exp[-2]

            inverse_op = inverse[op]

            lhop = eval(f"{lhop} {inverse_op} {num}")
            exp = " ".join(split_exp[:-2])


        elif valid_number(split_exp[0], allow_x=False):
            num = split_exp[0]
            op = split_exp[1]

            inverse_op = inverse[op]

            lhop = eval(f"{lhop} {inverse_op} {num}")
            exp = " ".join(split_exp[2:])

    return int(lhop)


                           

            



def solve(data):

    data = [row.replace("+", "==") if row.startswith("root:") else row for row in data]

    def try_eval(exp):


        try:
            return rpn_eval(exp)
        except Exception as e:
            return exp

    def prep(exp):
        

        return try_eval(rpn_convert(exp))
  
            
    count = 0

    jobs = {}

    attempt = MIN_ATTEMPT
    

    [jobs.update({row.split(": ")[0]:prep(row.split(": ")[1])}) for row in data]

    orig_jobs = dict(jobs)

    last_to_resolve = None

    jobs["humn"] = "x"


    for op in "-+*/":
        jobs["root"] = jobs["root"].replace(op, "==")
    

    

    to_resolve = jobs

    complete = False
    while not complete:

        to_resolve = {m:j for m,j in jobs.items() if type(j)==str}

   

        for monkey, job in jobs.items():

                if type(job) != str:    continue

                terms = findall("[a-z]{4}", job)

                for t in terms:

                    job = str(job.replace(t, str(try_eval(jobs[t]))))


                jobs[monkey] = try_eval(job)


        if all(i.isdigit() or i in "x*-+/==" for i in jobs["root"].split()):
            complete = True



        



    return solve_rpn_simultaneous(jobs["root"])
            






if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    MIN_ATTEMPT = 0
    if p.check(TESTS, solve):
        MIN_ATTEMPT = -99999
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
