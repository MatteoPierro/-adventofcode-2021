import unittest

import re
from collections import defaultdict

from advent_of_code.utilities import read_lines
from itertools import product


def parse_target_area(raw_target_area):
    match = re.search('.* x=(?P<min_x>\d+)..(?P<max_x>\d+), y=(?P<min_y>-\d+)..(?P<max_y>-\d+)', raw_target_area)
    min_x = int(match.group('min_x'))
    max_x = int(match.group('max_x'))
    min_y = int(match.group('min_y'))
    max_y = int(match.group('max_y'))
    return TargetArea(min_x, max_x, min_y, max_y)


class TargetArea:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def contains(self, point):
        return self.min_x <= point[0] <= self.max_x and self.min_y <= point[1] <= self.max_y


class Probe:
    def __init__(self, velocity, position=(0, 0)):
        self.velocity = velocity
        self.position = position

    def move(self):
        (dx, dy) = self.velocity
        (x, y) = self.position
        new_position = (x + dx, y + dy)
        new_dx = update_x_velocity(x, dx)
        new_dy = dy - 1
        new_velocity = (new_dx, new_dy)
        return Probe(new_velocity, new_position)


def update_x_velocity(current_x, current_velocity):
    if current_velocity == 0:
        return 0
    if current_x < 0:
        return current_velocity + 1
    return current_velocity - 1


def find_maximum_y_position(target_area):
    valid_initial_velocities = set()
    trajectories = defaultdict(lambda: [])
    for initial_velocity in product(range(-300, 300), range(-300, 300)):
        probe = Probe(initial_velocity)
        while probe.position[0] <= target_area.max_x and probe.position[1] >= target_area.min_y:
            trajectories[initial_velocity].append(probe.position)
            if target_area.contains(probe.position):
                valid_initial_velocities.add(initial_velocity)
            probe = probe.move()
    maximum_y_positions = [max([position[1] for position in trajectories[velocity]]) for velocity in
                           valid_initial_velocities]
    return max(maximum_y_positions), len(valid_initial_velocities)


class TrickShotTest(unittest.TestCase):
    def test_contains(self):
        target_area = parse_target_area('target area: x=20..30, y=-10..-5')
        self.assertTrue(target_area.contains((25, -7)))
        self.assertFalse(target_area.contains((15, -7)))

    def test_move_probe(self):
        target_area = parse_target_area('target area: x=20..30, y=-10..-5')
        p = Probe((7, 2)).move().move().move().move().move().move().move()
        self.assertTrue(target_area.contains(p.position))

    def test_find_maximum_y_position(self):
        target_area = parse_target_area('target area: x=20..30, y=-10..-5')
        max_y_position, number_of_valid_initial_velocities = find_maximum_y_position(target_area)
        self.assertEqual(45, max_y_position)
        self.assertEqual(112, number_of_valid_initial_velocities)

    def test_puzzles(self):
        raw_target_area = read_lines('input_day17.txt')[0]
        target_area = parse_target_area(raw_target_area)
        max_y_position, number_of_valid_initial_velocities = find_maximum_y_position(target_area)
        self.assertEqual(25200, max_y_position)
        self.assertEqual(3012, number_of_valid_initial_velocities)
