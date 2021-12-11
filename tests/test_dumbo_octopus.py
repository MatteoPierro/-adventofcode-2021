import unittest
from advent_of_code.utilities import read_lines

from itertools import product

RELATIVE_NEIGHBORS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


def parse_energy_level_row(row):
    return [int(level) for level in row]


class World:
    def __init__(self, levels):
        self.levels = levels
        self.flashes = 0

    def tick(self):
        flashing_points = []
        already_flashed_points = []
        for (x, y) in product(range(10), range(10)):
            self.tick_point(already_flashed_points, flashing_points, x, y)
        self.increase_neighbors(flashing_points, already_flashed_points)

    def increase_neighbors(self, flashing_points, already_flashed_points):
        if len(flashing_points) == 0:
            return
        flashing_point = flashing_points.pop(0)
        neighbors = self.find_neighbors(flashing_point)
        for n in neighbors:
            if n in already_flashed_points:
                continue
            self.tick_point(already_flashed_points, flashing_points, n[0], n[1])
        return self.increase_neighbors(flashing_points, already_flashed_points)

    def tick_point(self, already_flashed_points, flashing_points, x, y):
        self.levels[y][x] += 1
        if self.levels[y][x] == 10:
            self.levels[y][x] = 0
            self.flashes += 1
            flashing_points.append((x, y))
            already_flashed_points.append((x, y))

    def find_neighbors(self, point):
        potential_neighbours = [(point[0] + r[0], point[1] + r[1]) for r in RELATIVE_NEIGHBORS]
        return [p for p in potential_neighbours if 0 <= p[0] < 10 and 0 <= p[1] < 10]

    def __str__(self):
        lines = [''.join([str(v) for v in level]) for level in self.levels]
        return "\n".join(lines)


class DumboOctopusTest(unittest.TestCase):

    def test_world_tick(self):
        raw_energy_levels = [
            '5483143223',
            '2745854711',
            '5264556173',
            '6141336146',
            '6357385478',
            '4167524645',
            '2176841721',
            '6882881134',
            '4846848554',
            '5283751526'
        ]

        energy_levels = [parse_energy_level_row(r) for r in raw_energy_levels]
        world = World(energy_levels)
        for _ in range(100):
            world.tick()
        expected_world_after_100_ticks = ['0397666866',
                                          '0749766918',
                                          '0053976933',
                                          '0004297822',
                                          '0004229892',
                                          '0053222877',
                                          '0532222966',
                                          '9322228966',
                                          '7922286866',
                                          '6789998766']
        self.assertEqual('\n'.join(expected_world_after_100_ticks), str(world))
        self.assertEqual(1656, world.flashes)

    def test_puzzle_1(self):
        raw_energy_levels = read_lines('input_day11.txt')
        energy_levels = [parse_energy_level_row(r) for r in raw_energy_levels]
        world = World(energy_levels)
        for _ in range(100):
            world.tick()
        self.assertEqual(1640, world.flashes)