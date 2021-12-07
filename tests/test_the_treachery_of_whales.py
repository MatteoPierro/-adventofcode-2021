import unittest
from advent_of_code.utilities import read_lines
from collections import Counter


def calculate_min_fuel(crabs, fuel_consumption_calculator=lambda distance: distance):
    lower_position = min(crabs)
    higher_position = max(crabs)
    crabs_by_positions = Counter(crabs)
    min_fuel = float('+inf')
    for position in range(lower_position, higher_position + 1):
        current_fuel = 0
        for (crabs_position, crabs) in crabs_by_positions.items():
            current_fuel += crabs * fuel_consumption_calculator(abs(crabs_position - position))
        if current_fuel < min_fuel:
            min_fuel = current_fuel
    return min_fuel


class ExtendedFullConsumption:
    def __init__(self):
        self.memo_fuel_consumptions = {}

    def consumption(self, distance):
        if distance not in self.memo_fuel_consumptions:
            fuel_consumption = sum(range(0, distance + 1))
            self.memo_fuel_consumptions[distance] = fuel_consumption
        return self.memo_fuel_consumptions[distance]


class TheTreacheryOfWhalesTest(unittest.TestCase):
    def test_puzzles(self):
        crabs = [int(position) for position in read_lines('input_day7.txt')[0].split(',')]
        self.assertEqual(356179, calculate_min_fuel(crabs))
        fuel_consumption = ExtendedFullConsumption()
        self.assertEqual(99788435, calculate_min_fuel(crabs, fuel_consumption.consumption))
