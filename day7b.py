from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 7
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k///24933642"""

DEBUG = True

from uuid import uuid4

memo = {}

class Folder:

    def __init__(self, name, parent=None):
        self.name = name
        self.sub_folders = []
        self.files = []
        self.parent = parent
        self.size = 0
        self.id = uuid4()

    def __repr__(self):
        return self.name

    def get(self, child_name):
        for child in self.sub_folders:
            if str(child) == child_name:
                return child
        else:
            raise Exception(f"{self.name} directory does not contain directory called {child_name}")

class FileTree:

    def __init__(self):

        self.root = None


    def create_folder(self, name, parent=None):

        folder = Folder(name, parent)

        if self.root is None:
            self.root = folder
        else:
            if not parent:
                parent = self.root
            parent.sub_folders.append(folder)
        
        return folder


    def display(self, depth=0, folder=None):
        out = ""

        if folder is None:
            folder = self.root
        
        for file in folder.files:
            print(" "*(depth),'-', file["fn"], (f"(file, size={file['size']})"))

        for sub_folder in folder.sub_folders:
            print(" "*depth, '-',sub_folder.name)
            self.display(depth+1, sub_folder)

    def calculate_size(self, folder=None):
        size = 0
        if folder is None:
            folder = self.root
            
        for sub_folder in folder.sub_folders:
            size += self.calculate_size(sub_folder)

        size += sum(file["size"] for file in folder.files)

        folder.size = size
        
        return size

    def walk(self, acceptable, folder=None, minimimum=0):
        
        if folder is None:
            folder = self.root
            minimimum =  30000000 - (70000000 - folder.size)

        for sub_folder in folder.sub_folders:
            self.walk(acceptable, sub_folder, minimimum)

        if folder.size >= minimimum:
            acceptable[folder.id] = folder.size

        return acceptable
     


def solve(data):

    my_files = FileTree()

    current_dir = my_files.create_folder("/")
    
    depth = 0
    
    for line in data[1:]:

        if line.startswith("$ cd .."):     
            current_dir = current_dir.parent           
            depth -= 1

        elif line.startswith("$ cd"):
            depth += 1
            name = line.split()[-1]
            current_dir = current_dir.get(name)
                         
        elif line.startswith("dir"):
            name = line.split()[-1]
            my_files.create_folder(name, parent=current_dir)
            
        elif line.split()[0].isdigit():
            size, fn = line.split()
            current_dir.files.append({"fn":fn, "size":int(size)})

    my_files.display()

    my_files.calculate_size()

    acceptable = my_files.walk({})

    return min(acceptable.values())
        
    

    



acceptable = {}
if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        acceptable = {}
        
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        
        print("FINAL ANSWER: ", solve(puzzle_input))
