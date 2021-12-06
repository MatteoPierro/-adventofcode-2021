import unittest
from collections import Counter

from advent_of_code.utilities import read_lines


def evolve(initial_population, iterations=1):
    timers_occurrences = Counter(initial_population)
    for _ in range(iterations):
        first_timer = timers_occurrences[0]
        for timer_index in range(8):
            timers_occurrences[timer_index] = timers_occurrences[timer_index + 1]
        timers_occurrences[6] += first_timer
        timers_occurrences[8] = first_timer
    return timers_occurrences


def population_size_after_evolution(initial_population, iterations):
    return sum(evolve(initial_population, iterations).values())


def read_initial_population():
    return list(map(int, read_lines('input_day6.txt')[0].split(',')))


class LanternfishTest(unittest.TestCase):
    def test_evolve(self):
        initial_population = [3, 4, 3, 1, 2]
        self.assertEqual(5934, population_size_after_evolution(initial_population, 80))
        self.assertEqual(26984457539, population_size_after_evolution(initial_population, 256))

    def test_puzzle1(self):
        self.assertEqual(374994, population_size_after_evolution(read_initial_population(), 80))

    def test_puzzle2(self):
        self.assertEqual(1686252324092, sum(evolve(read_initial_population(), 256).values()))
