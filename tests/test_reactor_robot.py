import unittest
from itertools import product
import re

from advent_of_code.utilities import read_lines

STEP_TEMPLATE = '(?P<reboot_switch>\w+) x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+),' \
                'y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+),' \
                'z=(?P<z_min>-?\d+)..(?P<z_max>-?\d+)'


def parse_input(raw_input):
    match = re.search(STEP_TEMPLATE, raw_input)
    reboot_switch = match.group('reboot_switch')
    x_min = int(match.group('x_min'))
    x_max = int(match.group('x_max'))
    y_min = int(match.group('y_min'))
    y_max = int(match.group('y_max'))
    z_min = int(match.group('z_min'))
    z_max = int(match.group('z_max'))
    limits = [(x_min, x_max),
              (y_min, y_max),
              (z_min, z_max)]
    return reboot_switch, limits


def operate_reboot(reboot_switch, limits, already_on):
    limits = [(max(-50, a[0]), min(50, a[1])) for a in limits]
    for x, y, z in product(range(limits[0][0], limits[0][1] + 1),
                           range(limits[1][0], limits[1][1] + 1),
                           range(limits[2][0], limits[2][1] + 1)):
        if reboot_switch == 'on':
            already_on.add((x, y, z))
        else:
            already_on.discard((x, y, z))
    return already_on


class ReactorRebootTest(unittest.TestCase):
    def test_simple_input(self):
        reboot_steps = ['on x=10..12,y=10..12,z=10..12',
                        'on x=11..13,y=11..13,z=11..13',
                        'off x=9..11,y=9..11,z=9..11',
                        'on x=10..10,y=10..10,z=10..10']
        reboot_switch, limits = parse_input(reboot_steps[0])
        self.assertEqual('on', reboot_switch)
        self.assertEqual(limits, [(10, 12), (10, 12), (10, 12)])
        reboot_switch, limits = parse_input(reboot_steps[2])
        self.assertEqual('off', reboot_switch)
        self.assertEqual(limits, [(9, 11), (9, 11), (9, 11)])
        already_on = set()
        for reboot_step in reboot_steps:
            reboot_switch, limits = parse_input(reboot_step)
            already_on = operate_reboot(reboot_switch, limits, already_on)
        self.assertEqual(39, len(already_on))

    def test_puzzle1(self):
        reboot_steps = read_lines('input_day22.txt')
        already_on = set()
        for reboot_step in reboot_steps:
            reboot_switch, limits = parse_input(reboot_step)
            already_on = operate_reboot(reboot_switch, limits, already_on)
        self.assertEqual(564654, len(already_on))

    def test_overlap_area(self):
        v1 = Volume((1, 5), (0, 10), (-10, 7))  # x_range, y_range, z_range
        v2 = Volume((2, 6), (10, 20), (5, 20))
        self.assertTrue(v1.overlaps(v2))
        self.assertTrue(v2.overlaps(v1))
        v1 = Volume((1, 5), (0, 0), (0, 0))
        v2 = Volume((7, 10), (0, 0), (0, 0))
        self.assertFalse(v1.overlaps(v2))
        self.assertFalse(v2.overlaps(v1))
        v1 = Volume((1, 5), (0, 10), (0, 0))
        v2 = Volume((2, 6), (20, 30), (0, 0))
        self.assertFalse(v1.overlaps(v2))
        self.assertFalse(v2.overlaps(v1))
        v1 = Volume((1, 5), (0, 10), (0, 10))
        v2 = Volume((2, 6), (0, 10), (20, 30))
        self.assertFalse(v1.overlaps(v2))
        self.assertFalse(v2.overlaps(v1))
        v1 = Volume((-1, 5), (0, 10), (0, 0))
        v2 = Volume((2, 6), (0, 10), (0, 0))
        v1.subtract(v2)
        self.assertEqual(33, v1.volume())

    def test_calculate_volumes(self):
        reboot_steps = read_lines('input_day22_test.txt')
        areas_on = []
        for reboot_step in reboot_steps:
            reboot_switch, limits = parse_input(reboot_step)
            v = Volume(limits[0], limits[1], limits[2])
            for vv in areas_on:
                vv.subtract(v)
            if reboot_switch == 'on':
                areas_on.append(v)
        self.assertEqual(2758514936282235, sum([v.volume() for v in areas_on]))

    def test_puzzle2(self):
        reboot_steps = read_lines('input_day22.txt')
        areas_on = []
        for reboot_step in reboot_steps:
            reboot_switch, limits = parse_input(reboot_step)
            v = Volume(limits[0], limits[1], limits[2])
            for vv in areas_on:
                vv.subtract(v)
            if reboot_switch == 'on':
                areas_on.append(v)
        self.assertEqual(1214193181891104, sum([v.volume() for v in areas_on]))


class Volume:
    def __init__(self, x_range, y_range, z_range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.to_remove = []

    def overlaps(self, other):
        if not (self.x_range[0] <= other.x_range[1] <= self.x_range[1] or
                other.x_range[0] <= self.x_range[1] <= other.x_range[1]):
            return False
        if not (self.y_range[0] <= other.y_range[1] <= self.y_range[1] or
                other.y_range[0] <= self.y_range[1] <= other.y_range[1]):
            return False
        if not (self.z_range[0] <= other.z_range[1] <= self.z_range[1] or
                other.z_range[0] <= self.z_range[1] <= other.z_range[1]):
            return False
        return True

    def subtract(self, other):
        if not self.overlaps(other):
            return
        x_min = max(self.x_range[0], other.x_range[0])
        x_max = min(self.x_range[1], other.x_range[1])
        y_min = max(self.y_range[0], other.y_range[0])
        y_max = min(self.y_range[1], other.y_range[1])
        z_min = max(self.z_range[0], other.z_range[0])
        z_max = min(self.z_range[1], other.z_range[1])
        overlap_volume = Volume((x_min, x_max), (y_min, y_max), (z_min, z_max))
        for v in self.to_remove:
            v.subtract(overlap_volume)
        self.to_remove.append(overlap_volume)

    def volume(self):
        volume_to_remove = sum([v.volume() for v in self.to_remove])
        return ((abs(self.x_range[1] - self.x_range[0]) + 1) * (abs(self.y_range[1] - self.y_range[0]) + 1) * (abs(
            self.z_range[1] - self.z_range[0]) + 1)) - volume_to_remove
