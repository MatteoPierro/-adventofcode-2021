import unittest
from advent_of_code.utilities import read_lines
from itertools import product
from functools import reduce
import operator

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


def calculate_basin_for_low_point(low_point_coordinates, heightmap, basin):
    nx = len(heightmap[0])
    ny = len(heightmap)
    (x, y) = low_point_coordinates
    if x >= nx or x < 0:
        return basin
    if y >= ny or y < 0:
        return basin
    if heightmap[y][x] == 9:
        return basin
    if (x, y) in basin:
        return basin
    basin.append(low_point_coordinates)
    calculate_basin_for_low_point((x - 1, y), heightmap, basin)
    calculate_basin_for_low_point((x + 1, y), heightmap, basin)
    calculate_basin_for_low_point((x, y + 1), heightmap, basin)
    calculate_basin_for_low_point((x, y - 1), heightmap, basin)
    return basin


def product_top_three_basin_lengths(heightmap):
    low_points_coordinates = find_low_points_coordinates(heightmap)
    top_three_basin_lengths = sorted(
        [len(calculate_basin_for_low_point(lp, heightmap, [])) for lp in low_points_coordinates])[
                              -3:]
    return reduce(operator.mul, top_three_basin_lengths, 1)


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
        self.assertEqual(1134, product_top_three_basin_lengths(heightmap))

    def test_puzzle2(self):
        raw_heightmap = read_lines('input_day9.txt')
        heightmap = [parse_heightmap_row(row) for row in raw_heightmap]
        self.assertEqual(1059300, product_top_three_basin_lengths(heightmap))
