import unittest
from advent_of_code.utilities import read_lines
from collections import Counter


def calculate_min_fuel(crabs):
    lower_position = min(crabs)
    higher_position = max(crabs)
    crabs_by_positions = Counter(crabs)
    min_fuel = float('+inf')
    for position in range(lower_position, higher_position + 1):
        current_fuel = 0
        for (crabs_position, crabs) in crabs_by_positions.items():
            current_fuel += crabs * abs(crabs_position - position)
        if current_fuel < min_fuel:
            min_fuel = current_fuel
    return min_fuel


class TheTreacheryOfWhalesTest(unittest.TestCase):
    def test_calculate_min_fuel(self):
        crabs = [int(position) for position in read_lines('input_day7.txt')[0].split(',')]
        self.assertEqual(356179, calculate_min_fuel(crabs))
