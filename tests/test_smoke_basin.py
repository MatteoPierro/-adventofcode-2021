import unittest
from advent_of_code.utilities import read_lines
from itertools import product

NEIGHBOURS_RELATIVE_POSITIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse_heightmap_row(row):
    return [int(value) for value in row]


def calculate_possible_neighbours_positions(point):
    return [(point[0] + n[0], point[1] + n[1]) for n in NEIGHBOURS_RELATIVE_POSITIONS]


def calculate_risk_level(raw_heightmap):
    heightmap = [parse_heightmap_row(row) for row in raw_heightmap]
    risk_level = 0
    max_y = len(heightmap)
    max_x = len(heightmap[0])
    for (x, y) in product(range(max_x), range(max_y)):
        possible_neighbours_positions = calculate_possible_neighbours_positions((x, y))
        neighbours_positions = [n for n in possible_neighbours_positions if
                                (0 <= n[0] < max_x and 0 <= n[1] < max_y)]
        neighbours = [heightmap[n[1]][n[0]] for n in neighbours_positions]
        min_neighbour = min(neighbours)
        point = heightmap[y][x]
        if point < min_neighbour:
            risk_level += point + 1
    return risk_level


def find_low_points_coordinates(heightmap):
    low_points = []
    max_y = len(heightmap)
    max_x = len(heightmap[0])
    for (x, y) in product(range(max_x), range(max_y)):
        possible_neighbours_positions = calculate_possible_neighbours_positions((x, y))
        neighbours_positions = [n for n in possible_neighbours_positions if
                                (0 <= n[0] < max_x and 0 <= n[1] < max_y)]
        neighbours = [heightmap[n[1]][n[0]] for n in neighbours_positions]
        min_neighbour = min(neighbours)
        point = heightmap[y][x]
        if point < min_neighbour:
            low_points.append((x, y))
    return low_points


def calculate_basin_for_low_point(heightmap, low_point):
    max_y = len(heightmap)
    max_x = len(heightmap[0])
    basin = []
    for x in range(low_point[0], max_x):
        if heightmap[low_point[1]][x] == 9:
            break
        for y in reversed(range(0, low_point[1])):
            print(f"position {(x, y)}: value {heightmap[y][x]}")
            if heightmap[y][x] == 9:
                break
            basin.append((x, y))
        for y in range(low_point[1], max_y):
            print(f"position {(x, y)}: value {heightmap[y][x]}")
            if heightmap[y][x] == 9:
                break
            basin.append((x, y))
    for x in reversed(range(0, low_point[0])):
        if heightmap[low_point[1]][x] == 9:
            break
        for y in reversed(range(0, low_point[1])):
            print(f"position {(x, y)}: value {heightmap[y][x]}")
            if heightmap[y][x] == 9:
                break
            basin.append((x, y))
        for y in range(low_point[1], max_y):
            print(f"position {(x, y)}: value {heightmap[y][x]}")
            if heightmap[y][x] == 9:
                break
            basin.append((x, y))
    return basin


class SmokeBasinTest(unittest.TestCase):
    def test_calculate_risk_level(self):
        raw_heightmap = ['2199943210',
                         '3987894921',
                         '9856789892',
                         '8767896789',
                         '9899965678']
        self.assertEqual(15, calculate_risk_level(raw_heightmap))

    def test_puzzle1(self):
        raw_heightmap = read_lines('input_day9.txt')
        self.assertEqual(486, calculate_risk_level(raw_heightmap))

    def test_find_low_points(self):
        raw_heightmap = ['2199943210',
                         '3987894921',
                         '9856789892',
                         '8767896789',
                         '9899965678']
        heightmap = [parse_heightmap_row(row) for row in raw_heightmap]
        low_points_coordinates = find_low_points_coordinates(heightmap)
        self.assertEqual([(1, 0), (2, 2), (6, 4), (9, 0)], low_points_coordinates)
        low_points = [heightmap[n[1]][n[0]] for n in low_points_coordinates]
        self.assertEqual([1, 5, 5, 0], low_points)
        self.assertEqual([(1, 0), (0, 0), (0, 1)], calculate_basin_for_low_point(heightmap, low_points_coordinates[0]))
        self.assertEqual([(6, 3), (6, 4), (7, 3), (7, 2), (7, 4), (8, 3), (8, 4), (9, 4), (5, 4)],
                         calculate_basin_for_low_point(heightmap, low_points_coordinates[-2]))
        self.assertEqual([(9, 0), (9, 1), (9, 2), (8, 0), (8, 1), (7, 0), (6, 0), (6, 1), (5, 0)],
                         calculate_basin_for_low_point(heightmap, low_points_coordinates[-1]))
        self.assertEqual([(1, 0), (0, 0), (0, 1)], calculate_basin_for_low_point(heightmap, low_points_coordinates[1]))
