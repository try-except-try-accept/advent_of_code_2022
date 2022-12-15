from re import search, match, findall
from collections import Counter
from helpers import PuzzleHelper

PP_ARGS = False, False #rotate, cast int

DAY = 15
TEST_DELIM = "---"
FILE_DELIM = "\n"
TESTS = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3///26"""

DEBUG = True

row_min, row_max = 0, 0


def set_row_min_max(x, y):
    global row_min, row_max

    if x < row_min:

        row_min = x

    elif x > row_max:
        row_max = x


def compute_points(a, b):

    #print("Computing points between", a, "and", b)

    x1, y1 = a
    x2, y2 = b
    x_diff = abs(x2 - x1)
    y_diff = abs(y2 - y1)
    x_inc = 1 if x1 < x2 else -1
    y_inc = 1 if y1 < y2 else -1

    if abs(x_diff) > abs(y_diff):
        #print("more x to change")

        x_inc = x_diff / y_diff

    else:
        #print("more y to change")
        y_inc = y_diff / x_diff

    #print("will change x by", x_inc, "and y by", y_inc)

    x_dec = False
    x_dec = x1 > x2

    y_dec = False
    y_dec = y1 > y2
    
    pts = set()

    done = False
    while not done:
        pts.add((int(x1), int(y1)))
        
        if x_dec:
            x1 -= x_inc
        else:
            x1 += x_inc

        if y_dec:
            y1 -= y_inc
        else:
            y1 += y_inc
        

        if x_dec and x1 < x2 or not x_dec and x1 > x2 or y_dec and y1 < y2 or not y_dec and y1 > y2:
            
            return pts

    


       


def display(poly, sensor, beacon):

    
    min_x = min(poly.points)[0]
    max_x = max(poly.points)[0]
    min_y = min(poly.points, key=lambda y:y[1])[1]
    max_y = max(poly.points, key=lambda y:y[1])[1]
    s = ""
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            c = "."
            if (x, y) in poly.points:
                c = "#"

            elif (x, y) == (sensor.x, sensor.y):
                c = "S"

            elif (x, y) == (beacon.x, beacon.y):
                c = "B"

            s += c
        s += "\n"

    print(s)

            

        
    

class Sensor:

    def __init__(self, x, y):
        set_row_min_max(x, y)
        
        self.x = x
        self.y = y
        self.beacon = None
        self.impossible = None

        


    def get_impossible_beacons(self, beacon):
        self.beacon = beacon

        x_dist = abs(beacon.x-self.x)
        y_dist = abs(beacon.y-self.y)

        print("Beacon is at", beacon.x, ",", beacon.y)

        print("Therefore no beacons within this range:")



        self.polygon = [(-x_dist, self.y),
        (self.x, -y_dist),
        (x_dist, self.y),
        (self.x, y_dist)]

        
        

        


class Beacon:
    def __init__(self, x, y):
        set_row_min_max(x, y)
        self.x = x
        self.y = y


def solve(data):
    count = 0

    sensors = {}
    beacons = {}
    current_sensor = None
    impossible = set()

    for row in data:
        print(row)

        row = row.split()

        sx, sy, bx, by = row[2], row[3][:-1], row[8], row[9]
        print(sx, sy, bx, by)

        sensor_code = sx+sy

        new_sensor = eval(f"Sensor({sx} {sy})")

        sensors[sensor_code] = new_sensor

        current_sensor = new_sensor
        
        beacon_code = bx+by
        beacon = beacons.get(beacon_code)
        if beacon is None:
            beacon = eval(f"Beacon({bx} {by})")
        current_sensor.get_impossible_beacons(beacon)
        


        impossible.add(current_sensor.polygon)
    print("Processed sensors/beacons")

    all_bounds = []

    for poly in impossible:
        this_bounds = poly.get_row_bounds(Y_WANTED)
        if this_bounds is not None:
            all_bounds.append(this_bounds)

    impossible = set()

    for x1, x2 in all_bounds:
        impossible |= set(range(x1, x2+1))



    all_possible = set(range(row_min, row_max+1))

    print(all_possible)

    input()

 
    print("impossible", impossible)
    print("possible", all_possible, "entire row", len(all_possible), row_min, "to", row_max)

    return len(impossible)



compute_points((-100, 0), (-110, 50))


if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    Y_WANTED = 10

    if p.check(TESTS, solve):
        Y_WANTED = 2000000
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
