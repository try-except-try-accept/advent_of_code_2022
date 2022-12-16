from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper


PP_ARGS = False, False #rotate, cast int

DAY = 16
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II///1651"""

DEBUG = True


def calc_valve_distance(v1, v2, d=0, found=False, visited=None):

    return len(a_star_search(graph, v1, v2).nodes)

   


def a_star_search(goal, start):
    global table

    print("find way to", start, "from", goal)
    
    goal_node = v_map[goal]
    start_node = v_map[start]


    # get all distances    
    distances = [calculate_distance(n, goal_node) for n in v_map.values()]

    max_distance = max(distances)

    # set up table
                                
    table = {n:{"node":str(n),
                "g-cost":INF if n is not start_node else 0,
                "h-cost":calculate_distance(n, goal_node),
                "f-cost":INF,
                "prev":None, "calc":""} for n in v_map.values()}   

    # OPEN - the set of nodes to be evaluated
    # add the start node to open
    open_nodes = set([start_node])
    # CLOSED - the set of nodes already evaluated
    closed_nodes = set()
    current_node = None

    while len(open_nodes):
            #p.bugprint("open nodes looping")

            ## find the open list node with smallest known f-cost                    

            current_node = min(open_nodes, key=lambda n: table[n]["f-cost"])

            if current_node == goal_node:
                break

            ## remove current from OPEN
            open_nodes.remove(current_node)

            closed_nodes.add(current_node)

            ## find each un-closed neighbour of the current node

            #p.bugprint(f" i have {len(current_node.neighbours)} neighbours")
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

        
        #p.bugprint("im at", node)
        try:
            node = table[node]["prev"]
        except KeyError:
            return INF # some paths are impossible!
        path.append(node)

    path = list(reversed(path))
    path_copy = list(path)

    next_node = path_copy.pop(0)

    s = ""

    while path_copy:
        next_node = path_copy.pop()
        direction_map[next_node.y][next_node.x] = next_node.elevation.upper()

    length = len(path) + 1 - ERROR_CORRECT

        
    return length




v_map = None
    


class Valve:
    def __init__(self, label):
        self.label = label
        self.connections = []
        self.flow = 0
        self.open = False

    def get_eventual_pressure(self, current, min_remain):      
        distance = a_star_search(current, self)
        return ((min_remain-distance) * self.flow)

    def __repr__(self):
        return self.label

v_map = {}


def get_or_make_valve(label, v_map):

    valve = v_map.get(label)
    if valve is None:
        valve = Valve(label)
        v_map[label] = valve
        print("Added", label)

    return valve
    
    
    

def solve(data):
    global v_map
    count = 0

    minute = 1

    for line in data:

        line = line.replace("valves", "valve")
        
        this_valve = get_or_make_valve(line[6:8].strip(), v_map)
        
        flow = int(search("\d{1,3}", line).group())
        this_valve.flow = flow

        for v in line.split("to valve ")[1].split(","):           
            connected_valve = get_or_make_valve(v.strip(), v_map)
            this_valve.connections.append(connected_valve)
            
            


        
            

    current = v_map["AA"]
    current.open = None

    open_valves = []

    mins_required = 0

    
    for m in range(30, -1, -1):

        
            
        print(f"== Minute {30-m} ==")

        if mins_required:
            print("Was spent moving")
            mins_required -= 1
            continue
            

        # find the best eventual flow
        

        best = max([v for v in v_map.values() if v.open == False], key=lambda v: v.get_eventual_pressure(current, m))

        mins_required = distance = a_star_search(current, best)
        
        print("takes", mins_required, "to move from", current, "to", best)

        current = best

        current.open = True



        pressure = sum(v.flow for v in v_map.values() if v.open)

        print(f"Valves {','.join(v.label for v in v_map.values() if v.open)} are open, releasing {pressure} pressure.")
    
    

    return count




if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
