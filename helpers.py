from re import search, match, findall
from collections import Counter


GREEDY = "\[.+\]" # greedily match anything between [ and ]
LAZY = "\[.+?\]"  # lazily match anything between [ and ]

class PuzzleHelper:

    def __init__(self, day, test_delim, file_delim, debug, pp_args):
        self.day = day
        self.test_delim = test_delim
        self.file_delim = file_delim
        self.debug = debug
        self.pp_args = pp_args
    def bugprint(self, *s, end="\n"):
        if self.debug:
            for item in s:
                print(str(item), end=" ")
            print(end=end)


    def buginput(self, s=""):
        if self.debug:
            print(s)
            input()


    def load_puzzle(self):
        with open(f"day{self.day}.txt") as f:
            data = f.read()

        return data

    def pre_process(self, data, rotate=False, cast_int=True):


        if rotate:  print("Rotating data")
        data = [d for d in data.split(self.file_delim)]
        
        if rotate:
            cols = len(data[0])
            new = [""] * cols
            
            for row in data:
                for i in range(cols):
                    new[i] += row[i]

            data = new

        if not cast_int:
            return data
        
        numeric = all(d.isdigit() for d in data)
        
        if numeric:
            data = list(map(int, data))
        return data


    def check(self, tests, solve):

        success = True

        for row in tests.split(self.test_delim):
            if not len(row):    continue

            data, expected = row.split("///")
            data = self.pre_process(data, *self.pp_args)
            print(data, "should get", expected)
            
            outcome = solve(data)
            if str(outcome).strip() == expected.strip():
                print("Test passed")
            else:
                print("Test failed")
                success = False                
                print(outcome)
                raise Exception("failed the test data")

        return success

    def convert_arg(self, data):
        if set(data) == set(["█", "."]):
            data = data.replace(".", "0").replace("█", "1")
            data = int(data, 2)

        try:
            return int(data)                              # return integer value
        except ValueError:
            if data in "TrueFalseNone": return eval(data) # return bool/null flag
            return data                                   # return > / < string
        
    def process_test_args(self, data):

        data = tuple(map(self.convert_arg, data.split(",")))

        if len(data) == 1:  data = data[0]

        return data

        
            
    
   
               
    def module_tests(self, solution_funcs):


        try:
            with open(f"day{self.day}.tests", encoding="utf-8") as f:
                test_data = f.read()
        except FileNotFoundError:
            print("No module tests found")
            return

        if not input("Run module tests?"):
            return           
        

        test_num = 1
        func = None
        data = {}
        this_test = ""

        print(f"processing {test_data.count('test:')}")
        for line in test_data.splitlines():


            if "test:" in line:
                print(line)
                e = None
                if func:
                    
                    data = {arg:self.process_test_args(value) for arg, value in data.items()}
                    expected = data.pop("result")

                    print(data)

                    

                    

                    actual = eval(f"{func}(**data)", solution_funcs | locals())
         
                    if expected != actual:
                        print(this_test)
                        print(f"RECEIVED: {actual}\n EXPECTED {expected}")
                        print(f"received")
                        debinarise(actual)
                        raise Exception(f"Test number {test_num} failed\n{e}")
                    print(f"Test number {test_num} ({func}) PASSED 🎉")
                    test_num += 1

                    print()
                    
                    
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

        input("all module tests passed")

