import unittest

from advent_of_code.utilities import read_lines
from functools import reduce


class Position:
    def __init__(self, depth=0, horizontal=0):
        self.depth = depth
        self.horizontal = horizontal

    def forward(self, units):
        return Position(self.depth, self.horizontal + units)

    def up(self, units):
        return Position(self.depth - units, self.horizontal)

    def down(self, units):
        return Position(self.depth + units, self.horizontal)

    def dive(self):
        return self.depth * self.horizontal


class AimPosition(Position):
    def __init__(self, depth=0, horizontal=0, aim=0):
        super().__init__(depth, horizontal)
        self.aim = aim

    def forward(self, units):
        horizontal = self.horizontal + units
        depth = self.depth + self.aim * units
        return AimPosition(depth, horizontal, self.aim)

    def up(self, units):
        return AimPosition(self.depth, self.horizontal, self.aim - units)

    def down(self, units):
        return AimPosition(self.depth, self.horizontal, self.aim + units)


def dive(instructions, position=Position()):
    position = reduce(move, instructions, position)
    return position.dive()


def move(current_position, instruction):
    [command, raw_units] = instruction.split()
    units = int(raw_units)
    match command:
        case 'forward':
            return current_position.forward(units)
        case 'up':
            return current_position.up(units)
        case 'down':
            return current_position.down(units)
    return current_position


class DiveTest(unittest.TestCase):
    def test_dive(self):
        instructions = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']
        self.assertEqual(150, dive(instructions))

    def test_puzzle1(self):
        instructions = read_lines('input_day2.txt')
        self.assertEqual(1580000, dive(instructions))

    def test_dive_with_aim(self):
        instructions = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']
        self.assertEqual(900, dive(instructions, AimPosition()))

    def test_puzzle2(self):
        instructions = read_lines('input_day2.txt')
        self.assertEqual(1251263225, dive(instructions, AimPosition()))
