from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper
from math import inf as INF
try:
    from dijkstar import Graph, find_path
except:
    print("dijkstar not installed")


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
   


def dijkstra(start, goal):
    # Dijkstra's Algorithm
    origin = start
    # set up table
    table = {n:{"node":str(n), "cost":INF if n is not origin else 0, "prev":"", "calc":""} for n in v_map.values()}                        
    unvisited = list(v_map.values())
    visited = []

    print("From", start, "to", goal)

    while len(unvisited):

            smallest = INF
            current_node = None

            ## find the unvisited vertex with smallest known distance from the origin
            for node, data in table.items():
                    if node not in unvisited:        continue
                    if data["cost"] < smallest:
                            smallest = data["cost"]
                            current_node = node
            p.bugprint("The current vertex is", current_node)

            ## find each unvisited neighbour of the current vertex

            for neighbour in current_node.connections:
                    
                    p.bugprint(f"{current_node} is connected to {neighbour}")
                    if neighbour not in unvisited:
                            p.bugprint("Already visited")
                    else:
                            ## calculate total distance from origin node
                            tot = neighbour.weight
                            calc = str(tot)
                            # until we've got back to the start
                            p.bugprint(f"We need to make it back from {current_node} to {origin}")
                            pitstop = table[current_node]["cost"]
                            p.bugprint(f"Came via {current_node} and that cost {pitstop}")
                            tot += pitstop
                            calc += " + " + str(pitstop)
                            p.bugprint(f"so the total is now {tot}")

                            if tot < table[neighbour]["cost"]:
                                    table[neighbour]["prev"] = current_node                                                        
                                    table[neighbour]["cost"] = tot                                                                                                              
                                    table[neighbour]["calc"] = calc
                                    
                                    
                                    for node, data in table.items():
                                            p.bugprint(
                                                    f'{str(node)} \t\t {data["cost"]} \t\t {data["prev"]} \t\t {data["calc"]}')

                                    p.bugprint()
                            else:
                                    p.bugprint(f"{tot} was not shorter. table not updated")
            unvisited.remove(current_node)




            node = goal

            
    path = [str(goal)]

    while node is not origin:

            node = table[node]["prev"]
            path.append(str(node))

    return path


  

v_map = None
    


class Valve:
    def __init__(self, label):
        self.label = label
        self.connections = []
        self.flow = 0
        self.open = False
        self.weight = 1

    def get_eventual_pressure(self, current, min_remain):      
        distance = dijkstra(current, self)
        return ((min_remain-distance) * self.flow)

    def __repr__(self):
        return self.label

v_map = {}

def get_next_best_valve(current, minutes_left, best_map, d=0):


    for n in current.connections:
        if n in best_map:   continue

        best_map[n] = {"valve":n,
                       "pressure_potential":0 if n.open else n.flow * (minutes_left - d),
                      "distance":d}

        get_next_best_valve(n, minutes_left-1, best_map, d+1)

        

        

    

    


def get_or_make_valve(label, v_map):

    valve = v_map.get(label)
    if valve is None:
        valve = Valve(label)
        v_map[label] = valve
        p.bugprint("Added", label)

    return valve


g = None


 

def solve_2(data):
    global g
    g = Graph()

    # set up nodes

    node_data = {}

    for line in data:
        line = line.replace("valves", "valve")        
        this_valve = line[6:8].strip()     
        flow = int(search("\d{1,3}", line).group())
        path_weight = 1/flow if flow else 1

        node_data[this_valve] = {"flow":flow,
                                 "weight":path_weight,
                                 "connections":[]}

        
        for connected_valve in line.split("to valve ")[1].split(", "):
            node_data[this_valve]["connections"].append(connected_valve)



    for this_valve, data in node_data.items():

        for connected_valve in data["connections"]:
            weight = node_data[connected_valve]["weight"]
            g.add_edge(this_valve, connected_valve, (weight))
            print(f"I connected {this_valve} to {connected_valve}")

        
        

    current = "AA"



    all_valves = list(g)
    for m in range(30, -1, -1):
        # find highest pressure potential = next node

        for n in all_valves:
            if n == current:    continue

            path = find_path(g, current, n, cost_func=get_dist).nodes
            print(f"It takes {len(path)-1} steps to get to {n} path: {path}")
            
        paths = [(n, node_data[n]["flow"]*(m-(len(find_path(g, current, n).nodes)-1))) for n in all_valves]

        for p in paths:
            print(p)
        
        # find best path to next node

        # go to next node, turn on pitstop node IF node in top half of wanted nodes?
        print("Best valves to go to are", options)
        

def solve(data):
    global v_map
    count = 0

    minute = 1
    goal = None

    for line in data:
        line = line.replace("valves", "valve")        
        this_valve = get_or_make_valve(line[6:8].strip(), v_map)        
        flow = int(search("\d{1,3}", line).group())
        this_valve.flow = flow
        this_valve.weight = 1/flow if flow else 1

        if goal is None or this_valve.flow > goal.flow:
            goal = this_valve
        for v in line.split("to valve ")[1].split(","):           
            connected_valve = get_or_make_valve(v.strip(), v_map)
            this_valve.connections.append(connected_valve)            

    start = v_map["AA"]
    start.open = None


    for m in range(30):

        # find node with best pressure potential

        node = get_best_pressure_potential

        # this is J

        # find longest path to J

        # turn on interim nodes if node in top half of wanted

        

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)

    if p.check(TESTS, solve):
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
