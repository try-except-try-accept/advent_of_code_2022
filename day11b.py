from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import prod

PP_ARGS = False, False #rotate, cast int

DAY = 11
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1///2713310158"""




DEBUG = False

class Monkey:

    def __init__(self, i, data):

        self.num = i
        self.inspections = 0

        for line in data.splitlines():
            print(line)
            
            line = line.strip()
            if line.startswith("Starting"):
                self.items = list(map(int, line.replace("Starting items: ", "").split(", ")))
            elif line.startswith("Operation"):
                self.op = line.replace("Operation: new = ", "")
            elif line.startswith("Test"):
                self.test = int(line.split()[-1])
            elif line.startswith("If true:"):
                self.if_true = int(line.split()[-1])
            elif line.startswith("If false:"):
                self.if_false = int(line.split()[-1])

    def __repr__(self):
 
        return f"monkey {self.num} : items {self.items}, op {self.op}, test {self.test}, if true {self.if_true}, if false {self.if_false}"
            

    def inspect(self, monkeys, lcm):

        while self.items:
            self.inspections += 1

            item = self.items.pop(0)
            item = eval(self.op.replace("old", str(item)))
            
            item = item % lcm

            if item % self.test == 0:
                throw_to = self.if_true
            else:
                throw_to = self.if_false

            monkeys[throw_to].items.append(item)


        
                



def solve(data):
    count = 0

    data = "\n".join(data).split("Monkey ")[1:]

    monkeys = []

    for i, row in enumerate(data):
        monkeys.append(Monkey(i, row))


    all_tests = [m.test for m in monkeys]

    lcm = prod(all_tests)

    print("lcm is", lcm)
        
    current = 0
    for r in range(1, 10001):
        for m in monkeys:
            m.inspect(monkeys, lcm)
             

        if r in [1, 20, 1000]:
            p.bugprint(f"""After round {r}, the monkeys are holding items with these worry levels:""")
            for m in monkeys:
                p.bugprint(f"Monkey {m.num}: {m.items}")
                p.bugprint(f"inspected items {m.inspections} times")

            p.buginput()

    inspections = [m.inspections for m in monkeys]
    print(inspections)

    return prod(sorted(inspections)[-2:])




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
