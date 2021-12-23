import unittest
from copy import deepcopy, copy
from functools import cache
from queue import PriorityQueue


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@cache
def calculate_path(a, b):
    x_min = min(a[0], b[0])
    x_max = max(a[0], b[0])
    y_min = min(a[1], b[1])
    y_max = max(a[1], b[1])
    if a[0] == b[0] and a[1] != b[1]:
        path = {(a[0], y) for y in range(y_min, y_max + 1)}
    else:
        path = set()
        if a[1] == 0 or b[1] == 0 or a[0] != b[0]:
            path = path.union({(x, 0) for x in range(x_min, x_max + 1)})
        if a[1] != 0 and a[0] != b[0]:
            path = path.union({(a[0], y) for y in range(0, a[1] + 1)})
        if b[1] != 0 and a[0] != b[0]:
            path = path.union({(b[0], y) for y in range(0, b[1] + 1)})
    # path = path.union({(x_max, y) for y in range(1, y_max + 1)})
    # if a[1] != b[1]:
    #     path = path.union({(x, 0) for x in range(x_min, x_max + 1)})
    #     path = path.union({(x_min, y) for y in range(1, y_min + 1)})
    path.remove(a)
    return path


end_positions = {
    ((2, 1), 'A'),
    ((2, 2), 'A'),
    ((4, 1), 'B'),
    ((4, 2), 'B'),
    ((6, 1), 'C'),
    ((6, 2), 'C'),
    ((8, 1), 'D'),
    ((8, 2), 'D')}

bonus = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


class AmphipodTest(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(3, distance((0, 0), (2, 1)))
        self.assertEqual(6, distance((1, 0), (6, 1)))
        self.assertEqual(2, distance((8, 1), (9, 0)))
        self.assertEqual({(9, 0), (8, 0)}, calculate_path((8, 1), (9, 0)))
        # self.assertEqual({(9, 0), (8, 0)}, calculate_path((4, 2), (8, 2)))
        amphipod_positions = {((4, 1), 'C'), ((3, 0), 'A'), ((5, 0), 'B'), ((2, 1), 'B'), ((9, 0), 'D'), ((4, 2), 'D'),
                              ((6, 2), 'C'), ((2, 2), 'A')}
        path = calculate_path((4, 1), (6, 1))
        self.assertTrue(any(p in path for (p, _) in amphipod_positions))

    def test_calculate_path(self):
        self.assertEqual({(1, 0), (2, 0), (2, 1)}, calculate_path((0, 0), (2, 1)))
        self.assertEqual({(1, 0), (2, 0), (0, 0)}, calculate_path((2, 1), (0, 0)))
        self.assertEqual({(2, 2)}, calculate_path((2, 1), (2, 2)))
        self.assertEqual({(2, 1)}, calculate_path((2, 2), (2, 1)))
        self.assertEqual({(9, 0), (4, 0), (0, 0), (7, 0), (2, 0), (8, 0), (3, 0), (5, 0), (6, 0), (1, 0)},
                         calculate_path((10, 0), (0, 0)))
        self.assertEqual({(4, 0), (2, 1), (4, 1), (2, 0), (3, 0)}, calculate_path((2, 2), (4, 1)))
        self.assertEqual({(2, 0), (4, 0), (2, 1), (3, 0)}, calculate_path((4, 1), (2, 1)))
        self.assertEqual({(6, 2), (4, 0), (6, 1), (2, 0), (3, 0), (5, 0), (6, 0)}, calculate_path((1, 0), (6, 2)))

    def test_best_cost(self):
        queue = PriorityQueue()
        # amphipod_positions = {
        #     ((4, 1), 'A'),
        #     ((2, 2), 'A'),
        #     ((2, 1), 'B'),
        #     ((6, 2), 'C'),
        #     ((4, 2), 'B'),
        #     ((6, 1), 'C'),
        #     ((8, 1), 'D'),
        amphipod_positions = {
            ((2, 1), 'B'),
            ((2, 2), 'A'),
            ((4, 1), 'C'),
            ((4, 2), 'D'),
            ((6, 1), 'B'),
            ((6, 2), 'C'),
            ((8, 1), 'D'),
            ((8, 2), 'A')}
        queue.put((0, amphipod_positions, []))
        cost, pp = best_cost(queue, set())
        acc = amphipod_positions
        for p in pp:
            print(f"{acc - p} -> {p - acc}")
            acc = p
            print()
        self.assertEqual(12521, cost)

    def test_puzzle1(self):
        queue = PriorityQueue()
        amphipod_positions = {
            ((2, 1), 'A'),
            ((2, 2), 'C'),
            ((4, 1), 'D'),
            ((4, 2), 'D'),
            ((6, 1), 'C'),
            ((6, 2), 'B'),
            ((8, 1), 'A'),
            ((8, 2), 'B')}
        queue.put((0, amphipod_positions, []))
        cost, pp = best_cost(queue, set())
        self.assertEqual(15365, cost)

    def test_best_cost_extended(self):
        queue = PriorityQueue()
        # amphipod_positions = {
        #     ((4, 1), 'A'),
        #     ((2, 2), 'A'),
        #     ((2, 1), 'B'),
        #     ((6, 2), 'C'),
        #     ((4, 2), 'B'),
        #     ((6, 1), 'C'),
        #     ((8, 1), 'D'),
        amphipod_positions = {
            ((2, 1), 'B'),
            ((2, 2), 'D'),
            ((2, 3), 'D'),
            ((2, 4), 'A'),
            ((4, 1), 'C'),
            ((4, 2), 'C'),
            ((4, 3), 'B'),
            ((4, 4), 'D'),
            ((6, 1), 'B'),
            ((6, 2), 'B'),
            ((6, 3), 'A'),
            ((6, 4), 'C'),
            ((8, 1), 'D'),
            ((8, 2), 'A'),
            ((8, 3), 'C'),
            ((8, 4), 'A')}
        queue.put((0, amphipod_positions, []))
        cost, pp = best_cost_extended(queue, set())
        acc = amphipod_positions
        for p in pp:
            print(f"{acc - p} -> {p - acc}")
            acc = p
            print()
        self.assertEqual(12521, cost)


def best_cost_extended(queue, memo):
    while not queue.empty():
        current_cost, amphipod_positions, previous_paths = queue.get()
        if amphipod_positions == extended_end_positions:
            previous_paths.append(amphipod_positions)
            return current_cost, previous_paths
        memo.add(tuple(amphipod_positions))
        for amphipod_position in amphipod_positions:
            start, amphipod = amphipod_position
            new_amphipod_positions = amphipod_positions.copy()
            new_amphipod_positions.remove(amphipod_position)
            ## already in the right position
            if start[0] == DESTINATIONS_COLUMN[amphipod] and (
                    all(((DESTINATIONS_COLUMN[amphipod], c), amphipod) in amphipod_positions for c in
                        range(start[0], 5))):
                destinations = []
            else:
                destinations = []
                positions = [p for (p, _) in amphipod_positions]
                if (DESTINATIONS_COLUMN[amphipod], 4) not in positions:
                    destinations = [(DESTINATIONS_COLUMN[amphipod], 4)]
                elif (DESTINATIONS_COLUMN[amphipod], 3) not in positions and (
                        ((DESTINATIONS_COLUMN[amphipod], 4), amphipod)) in amphipod_positions:
                    destinations = [(DESTINATIONS_COLUMN[amphipod], 3)]
                elif (DESTINATIONS_COLUMN[amphipod], 2) not in positions and \
                        all(((DESTINATIONS_COLUMN[amphipod], c), amphipod) in amphipod_positions for c in
                            range(3, 5)):
                    destinations = [(DESTINATIONS_COLUMN[amphipod], 2)]
                elif (DESTINATIONS_COLUMN[amphipod], 1) not in positions and \
                        all(((DESTINATIONS_COLUMN[amphipod], c), amphipod) in amphipod_positions for c in
                            range(2, 5)):
                    destinations = [(DESTINATIONS_COLUMN[amphipod], 1)]
                if len(destinations) == 0 and start[1] != 0:
                    destinations = AISLE
            for destination in destinations:
                if start == destination:
                    continue
                path = calculate_path(start, destination)
                # print(path)
                if any(p in path for (p, _) in amphipod_positions):
                    # print('skip this solution')
                    continue
                else:
                    positions = copy(new_amphipod_positions)
                    positions.add((destination, amphipod))
                    new_cost = current_cost + bonus[amphipod] * len(path)
                    if tuple(positions) in memo:
                        # print('here')
                        continue
                    pp = copy(previous_paths)
                    pp.append(positions)
                    queue.put((new_cost, positions, pp))


def best_cost(queue, memo):
    while not queue.empty():
        current_cost, amphipod_positions, previous_paths = queue.get()
        if amphipod_positions == end_positions:
            previous_paths.append(amphipod_positions)
            return current_cost, previous_paths
        memo.add(tuple(amphipod_positions))
        for amphipod_position in amphipod_positions:
            start, amphipod = amphipod_position
            new_amphipod_positions = amphipod_positions.copy()
            new_amphipod_positions.remove(amphipod_position)
            ## already in the right position
            if start[0] == DESTINATIONS_COLUMN[amphipod] and (
                    start == (DESTINATIONS_COLUMN[amphipod], 2) or
                    ((DESTINATIONS_COLUMN[amphipod], 2), amphipod) in amphipod_positions):
                destinations = []
            else:
                destinations = []
                positions = [p for (p, _) in amphipod_positions]
                if (DESTINATIONS_COLUMN[amphipod], 2) not in positions:
                    destinations = [(DESTINATIONS_COLUMN[amphipod], 2)]
                elif (DESTINATIONS_COLUMN[amphipod], 1) not in positions and (
                        ((DESTINATIONS_COLUMN[amphipod], 2), amphipod)) in amphipod_positions:
                    destinations = [(DESTINATIONS_COLUMN[amphipod], 1)]
                if len(destinations) == 0 and start[1] != 0:
                    destinations = AISLE
            for destination in destinations:
                if start == destination:
                    continue
                path = calculate_path(start, destination)
                # print(path)
                if any(p in path for (p, _) in amphipod_positions):
                    # print('skip this solution')
                    continue
                else:
                    positions = copy(new_amphipod_positions)
                    positions.add((destination, amphipod))
                    new_cost = current_cost + bonus[amphipod] * len(path)
                    if tuple(positions) in memo:
                        # print('here')
                        continue
                    pp = copy(previous_paths)
                    pp.append(positions)
                    queue.put((new_cost, positions, pp))


extended_end_positions = {
    ((2, 1), 'A'),
    ((2, 2), 'A'),
    ((2, 3), 'A'),
    ((2, 4), 'A'),
    ((4, 1), 'B'),
    ((4, 2), 'B'),
    ((4, 3), 'B'),
    ((4, 4), 'B'),
    ((6, 1), 'C'),
    ((6, 2), 'C'),
    ((6, 3), 'C'),
    ((6, 4), 'C'),
    ((8, 1), 'D'),
    ((8, 2), 'D'),
    ((8, 3), 'D'),
    ((8, 4), 'D')}

AISLE = [(0, 0), (1, 0), (3, 0), (5, 0), (7, 0), (9, 0), (10, 0)]

DESTINATIONS_COLUMN = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}
