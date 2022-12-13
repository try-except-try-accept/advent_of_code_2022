from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import sqrt, inf as INF
from copy import deepcopy

PP_ARGS = False, False #rotate, cast int

DAY = 12
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Sabqponm
abcrzyxl
accsz{xk
acctuvwj
abdefghi///31
"""

DEBUG = False


UDLR =((0, -1),
       (0, 1),
       (-1, 0),
       (1, 0))

class Node:

    def __init__(self, elevation, x, y):
        self.x = x
        self.y = y
        self.elevation = elevation
        self.neighbours = []
        self.key = (x, y)

    def __repr__(self):
        return str(self.key)
    
def calculate_distance(node1, node2, mode=0):
    x1 = node1.x
    x2 = node2.x
    y1 = node1.y
    y2 = node2.y
    if mode == 0:
        #manhattan
        #
        return abs(x2-x1) - abs(y2-y1)

        #  You could start by moving down or right, but eventually you'll need to head toward the e at the bottom

        # does only y matter?

        #return abs(y2-y1)

    else:
        # euclidean        
        return sqrt((x2-x1) ** 2) + ((y2 - y1) ** 2)

def get_or_create_node(key, elevation, node_map):
    node = node_map.get(key)
    if node is None:
        node = Node(elevation, key[0], key[1])
        node_map[key] = node

    return node


        
node_map = None

def traverse(node, goal, path="", visited=None, success=None):
    p.bugprint(node.x, node.y)
    

    if visited is None:
        success = set()
        visited = set()



    path += node.elevation

    if node == goal:
        p.bugprint("Found a path!", path)
        success.add(path)

    

    unvisited = [n for n in node.neighbours if n not in visited]

    if not len(unvisited):  p.bugprint("nothing left to visit")

    for n in unvisited:
        visited.add(n)
        traverse(n, goal, path, visited, success)
        


    

        
    


def solve(data):
    global node_map
    count = 0

    node_map = {}

    WIDTH = len(data[0])
    HEIGHT = len(data)

    direction_map = [['.' for col in range(WIDTH)] for row in range(HEIGHT)]

    #direction_map = [list(row) for row in data]

    start = None

    ## set up graph
    for y, row in enumerate(data):
        for x, elevation in enumerate(row):
            key = (x, y)
            no_neighbours = False
            
            if elevation == "S":
                start = key
                elevation = "a"
            elif elevation == "{":
                goal = key                
                

            node = get_or_create_node(key, elevation, node_map)

            
            if no_neighbours:
                continue

            for change_x, change_y in UDLR:
                nx = x + change_x
                ny = y + change_y

                if nx >= WIDTH or nx < 0 or ny >= HEIGHT or ny < 0:
                    continue

                neighbour_elev = data[ny][nx]

                if (ord(neighbour_elev) - ord(elevation) > 1):
                    continue
                
                neigh_key = (nx, ny)
                
                neighbour = get_or_create_node(neigh_key, neighbour_elev, node_map)
                
                node.neighbours.append(neighbour)

    


    start_node = node_map[start]

    p.bugprint(type(start_node))
    end_node = node_map[goal]


    ## dijkstra's

    table = {node:[node,INF, None] for node in node_map.values()}

    table[start_node][1] = 0

    unvisited = set(node_map.values())

    p.bugprint(unvisited)

    while unvisited:
        possible = [row for row in table.values() if row[0] in unvisited]
        current = min(possible, key=lambda n: n[1])[0]
        if current == end_node:
            break

        p.bugprint("Current is", type(current))
        unvisited.remove(current)

        distance = table[current][1]

        for neighbour in current.neighbours:
            if neighbour not in unvisited:
                continue
            new_distance = distance + 1
            if new_distance < table[neighbour][1]:
                table[neighbour] = [neighbour, new_distance, current]
        


    for row in table.values():
        p.bugprint(row)

    current = table[end_node]

    steps = 0
    
    while node is not start_node:
        p.bugprint("is", node, start_node)
        node = current[2]
        direction_map[node.y][node.x] = node.elevation.upper()

        current = table[node]
        p.bugprint("Current is", current)
        steps += 1

    for row in direction_map:
        print("".join(row))

    return steps
        

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
