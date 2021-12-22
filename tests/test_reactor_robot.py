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
