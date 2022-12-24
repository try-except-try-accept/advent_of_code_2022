from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 23
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..///110"""

ELF = "#"

N_DIR = ((0, -1), (-1, -1), (1, -1))
S_DIR = ((0, 1), (-1, 1), (1, 1))
W_DIR = ((-1, 0), (-1, 1), (-1, -1))
E_DIR = ((1, 0), (1, 1), (1, -1))

ROUNDS = 10       

DEBUG = False

class Elf:
    def __init__(self, x, y, propositions, dir_list, elves):
        self.x = x
        self.y = y
        self.all_propositions = propositions
        self.dir_list = dir_list
        self.elves = elves

    def __repr__(self):
        return f"The elf at {self.x}, {self.y}"

    def first_half_of_round(self, all_propositions):
        p.bugprint(self, end="")

        self.all_propositions = all_propositions

        self.my_propositions = []

        for directions in self.dir_list:
            for xc, yc in directions:
                x, y = xc + self.x, yc + self.y
                if any((e.x, e.y) == (x, y) for e in self.elves):
                    p.bugprint("Can't move", directions[0])
                    break
            else:
                p.bugprint("Can move", directions[0])
                self.my_propositions.append((self.x+directions[0][0], self.y+directions[0][1]))
                

        if len(self.my_propositions) == 4:
            p.bugprint("didn't move - all sides free")
            self.my_propositions = []
        if self.my_propositions:
            self.all_propositions[self.my_propositions[0]] += 1

            p.bugprint("proposes", self.my_propositions[0])

    def second_half_of_round(self):
        p.bugprint(self, end="")
        if self.my_propositions:
            prop = self.my_propositions[0]
            if self.all_propositions[prop] == 1:
                self.x, self.y = prop[0], prop[1]
                p.bugprint("was the only one to move to", self.x, self.y)
            else:
                p.bugprint(self.all_propositions)
                p.bugprint("didn't move")

            self.my_propositions = []
        else:
            p.bugprint("Had no propositions")
            

######################

def display(elves, w, h):
    grid = [["." for x in range(-w, w*2)]for y in range(-h, h*2)]

    for e in elves:
        grid[e.y][e.x] = "#"

    for row in grid:
        print("".join(row))


######################

    
def solve(data):
    count = 0

    elves = []

    propositions = Counter()

    dir_list = [N_DIR, S_DIR, W_DIR, E_DIR]

    
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == ELF:
                elves.append(Elf(x+W_BUFFER, y+H_BUFFER, propositions, dir_list, elves))

    W = x + W_BUFFER
    H = y + H_BUFFER

    print("== Initial State ==")


    #display(elves, W, H)

    for round_num in range(1, ROUNDS+1):
        propositions = Counter()
        for elf in elves:
            elf.first_half_of_round(propositions)
        for elf in elves:
            elf.second_half_of_round()
            

        print(f"== End of Round {round_num}")

        #display(elves, W, H)



        dir_list.append(dir_list.pop(0))
        


    x_min = min(elves, key=lambda elf: elf.x).x
    x_max = max(elves, key=lambda elf: elf.x).x + 1
    y_min = min(elves, key=lambda elf: elf.y).y
    y_max = max(elves, key=lambda elf: elf.y).y + 1

    return ((x_max - x_min) * (y_max - y_min)) - len(elves)
    

    




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    W_BUFFER = 10
    H_BUFFER = 10
    if p.check(TESTS, solve):
        W_BUFFER = 50
        H_BUFFER = 50
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
