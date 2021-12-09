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
