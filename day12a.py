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
        self.neighbours = set()

    def __repr__(self):
        return f" at {self.x} {self.y} elevation: {self.elevation}"

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
                no_neighbours = True

            
            
##

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
                
                node.neighbours.add(neighbour)

    ## a* star algorithm

    
    goal_node = node_map[goal]
    start_node = node_map[start]

    # get all distances    
    distances = [calculate_distance(n, goal_node) for n in node_map.values()]

    max_distance = max(distances)


    # set up table



                                
    table = {n:{"node":str(n),
                "g-cost":INF if n is not start_node else 0,
                "h-cost":calculate_distance(n, goal_node),
                "f-cost":INF,
                "prev":None, "calc":""} for n in node_map.values()}   


    

    

    # OPEN - the set of nodes to be evaluated
    # add the start node to open
    open_nodes = set([start_node])
    # CLOSED - the set of nodes already evaluated
    closed_nodes = set()


    current_node = None

    while len(open_nodes):


            ## find the open list node with smallest known f-cost                    

            current_node = min(open_nodes, key=lambda n: table[n]["f-cost"])

            if current_node == goal_node:                    
                    break


            ## remove current from OPEN
            open_nodes.remove(current_node)

            ## add current to CLOSED
            closed_nodes.add(current_node)

            ## find each un-closed neighbour of the current node
            for neighbour in current_node.neighbours:


                    if neighbour in closed_nodes:
                            continue

                    g_cost = 1
                    calc = str(g_cost)        
                    pitstop = table[current_node]["g-cost"]

                    g_cost += pitstop
                                                            
                    calc += " + " + str(pitstop)                             
                    h_cost = table[neighbour]["h-cost"]                                        
                    calc += f" + {h_cost}"

                    f_cost = g_cost + h_cost

                    if neighbour not in open_nodes or g_cost < table[neighbour]["g-cost"]:
                            open_nodes.add(neighbour)
                            table[neighbour]["prev"] = current_node                                                        
                            table[neighbour]["f-cost"] = f_cost
                            table[neighbour]["g-cost"] = g_cost                                                                                
                            table[neighbour]["calc"] = calc

                    open_nodes.add(neighbour)

    destination = goal_node
    node = destination


    path = [destination]

    while node is not start_node:

        node = table[node]["prev"]
        path.append(node)

    path = list(reversed(path))
    
    path_copy = list(path)

    print(path_copy)

    next_node = path_copy.pop(0)

    s = ""

    while path_copy:
        next_node = path_copy.pop()
        direction_map[next_node.y][next_node.x] = next_node.elevation.upper()
        
        
    for row in direction_map:
        print("".join(row))
        


    return len(path) - 1





            
                
                
            

            

        
        

        
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
