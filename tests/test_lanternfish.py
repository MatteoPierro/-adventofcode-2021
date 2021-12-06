import unittest

from advent_of_code.utilities import read_lines


def evolve(current_population, iterations=1):
    if iterations == 0:
        return current_population
    new_population = []
    new_born = []
    for fish_timer in current_population:
        if fish_timer == 0:
            new_born.append(8)
            new_population.append(6)
        else:
            new_population.append(fish_timer - 1)
    return evolve(new_population + new_born, iterations - 1)


class LanternfishTest(unittest.TestCase):
    def test_evolve(self):
        initial_population = [3, 4, 3, 1, 2]
        self.assertEqual([2, 3, 2, 0, 1], evolve(initial_population))
        self.assertEqual([5, 6, 5, 3, 4, 5, 6, 7, 7, 8], evolve(initial_population, 5))
        self.assertEqual(5934, len(evolve(initial_population, 80)))

    def test_puzzle1(self):
        initial_population = list(map(int, read_lines('input_day6.txt')[0].split(',')))
        self.assertEqual(374994, len(evolve(initial_population, 80)))
