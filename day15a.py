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

DEBUG = False

row_min, row_max = 0, 0


def set_row_min_max(x, y):
    global row_min, row_max

    if x < row_min:
        row_min = x

    elif x > row_max:
        row_max = x

       

def display(polys, beacons, sensors, impossible):
    if not DEBUG:   return False
    s = ""
    p.bugprint(f"displaying {len(polys)} polys")
    p.bugprint("".join(chr(i) for i in range(38, 98)))
    for y in range(-10, 50):
        s += str(y).zfill(3) + " "
        for x in range(-10, 50+1):
            c = "."
            if x in impossible and y == Y_WANTED:
                c = "X"
            for pol in polys:
                if (x, y) == pol.left: c = "L"
                if (x, y) == pol.top: c = "U"
                if (x, y) == pol.bott: c = "D"
                if (x, y) == pol.right: c = "R"
                
            if any([(x, y) == (s.x, s.y) for s in sensors]):
                c = "S"
            if any([(x, y) == (b.x, b.y) for b in beacons]):
                c = "B"
            s += c
        s += "\n"
    p.bugprint(s)

def manhattan(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

class Polygon:

    def __init__(self, x, y, left, top, right, bott, dim):
        self.x = x
        self.y = y
        self.left = left
        self.top = top
        self.right = right
        self.bott = bott
        self.dim = dim
    

class Sensor:

    def __init__(self, x, y, polys):
        set_row_min_max(x, y)
        self.x = x
        self.y = y
        self.beacon = None
        self.impossible = None
        self.polys = polys

    def get_impossible_beacons(self, beacon):
        self.beacon = beacon
        dist = manhattan(self.x, self.y, beacon.x, beacon.y)
        p.bugprint("Beacon is at", beacon.x, ",", beacon.y)
        p.bugprint("Therefore no beacons within this range:")
        self.polys.append(Polygon(self.x, self.y,
                                 (self.x-dist, self.y),
                                 (self.x, self.y-dist),
                                 (self.x+dist, self.y),
                                 (self.x, self.y+dist),
                                  dist * 2))
 

class Beacon:
    def __init__(self, x, y):
        set_row_min_max(x, y)
        self.x = x
        self.y = y


def solve(data):
    count = 0

    sensors = {}
    beacons = {}
    polys = []
    current_sensor = None
    impossible = set()

    for row in data:
        p.bugprint(row)

        row = row.split()

        sx, sy, bx, by = row[2], row[3][:-1], row[8], row[9]
        p.bugprint(sx, sy, bx, by)

        sensor_code = sx+sy

        new_sensor = eval(f"Sensor({sx} {sy}, polys=polys)")
        sensors[sensor_code] = new_sensor
        current_sensor = new_sensor
        beacon_code = bx+by
        beacon = beacons.get(beacon_code)
        if beacon is None:
            beacon = eval(f"Beacon({bx} {by})")
            beacons[beacon_code] = beacon
        current_sensor.get_impossible_beacons(beacon)
        

    print("Processed sensors/beacons")
    all_bounds = []

    
    polys_affected = [poly for poly in polys if poly.top[1] < Y_WANTED and poly.bott[1] > Y_WANTED]

    impossible = set()
    for poly in polys_affected:
        x_adjust = abs((poly.dim // 2) - abs(poly.y - Y_WANTED))
        p.bugprint("x adjust is", x_adjust)
        impossible |= set(range(poly.x - x_adjust, poly.x + x_adjust + 1))

    print("Computed impossible coords")

    for obj in list(beacons.values()) + list(sensors.values()):
        if obj.y == Y_WANTED:
            impossible.remove(obj.x)

    display(polys_affected, beacons.values(), sensors.values(), impossible)
    
    return len(impossible)

if __name__ == "__main__":
    p = PuzzleHelper(DAY, TEST_DELIM, FILE_DELIM, DEBUG, PP_ARGS)
    Y_WANTED = 10

    if p.check(TESTS, solve):
        Y_WANTED = 2000000
        puzzle_input = p.load_puzzle()
        puzzle_input = p.pre_process(puzzle_input, *PP_ARGS)
        print("FINAL ANSWER: ", solve(puzzle_input))
