import unittest

from advent_of_code.utilities import read_lines
from functools import reduce


def dive(instructions):
    position = reduce(move, instructions, Position())
    return position.depth * position.horizontal


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


class DiveTest(unittest.TestCase):
    def test_dive(self):
        instructions = ['forward 5', 'down 5', 'forward 8', 'up 3', 'down 8', 'forward 2']
        self.assertEqual(150, dive(instructions))

    def test_puzzle1(self):
        instructions = read_lines('input_day2.txt')
        self.assertEqual(1580000, dive(instructions))