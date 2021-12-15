import unittest

from advent_of_code.utilities import read_lines
from collections import Counter


def parse_input(input):
    polymer_template = list(input[0])
    rules = {}
    raw_pair_insertion_rules = input[2:]
    for raw_pair_insertion_rule in raw_pair_insertion_rules:
        immediately_adjacent, to_insert = raw_pair_insertion_rule.split(' -> ')
        rules[tuple(immediately_adjacent)] = to_insert
    return polymer_template, rules


def evolve(raw_input, iterations):
    polymer_template, rules = parse_input(raw_input)
    symbols_occurrences = Counter(polymer_template)
    adjacent_occurrences = Counter(zip(polymer_template, polymer_template[1:]))
    for _ in range(iterations):
        adjacent_occurrences = evolve_adjacents(adjacent_occurrences, rules, symbols_occurrences)
    return symbols_occurrences


def evolve_adjacents(adjacent_occurrences, rules, symbols_occurrences):
    new_adjacents_occurrences = {}
    for (adjacent, intermediate) in rules.items():
        # rule adjacent not present in the current template
        if adjacent not in adjacent_occurrences.keys():
            continue
        adjacent_occurrence = adjacent_occurrences[adjacent]
        left = (adjacent[0], intermediate)
        right = (intermediate, adjacent[1])
        if left not in new_adjacents_occurrences:
            new_adjacents_occurrences[left] = 0
        if right not in new_adjacents_occurrences:
            new_adjacents_occurrences[right] = 0
        if intermediate not in symbols_occurrences.keys():
            symbols_occurrences[intermediate] = 0
        new_adjacents_occurrences[left] += adjacent_occurrence
        new_adjacents_occurrences[right] += adjacent_occurrence
        symbols_occurrences[intermediate] += adjacent_occurrence
    return new_adjacents_occurrences


class ExtendedPolymerizationTest(unittest.TestCase):
    def test_evolve(self):
        raw_input = ['NNCB',
                     '',
                     'CH -> B',
                     'HH -> N',
                     'CB -> H',
                     'NH -> C',
                     'HB -> C',
                     'HC -> B',
                     'HN -> C',
                     'NN -> C',
                     'BH -> H',
                     'NC -> B',
                     'NB -> B',
                     'BN -> B',
                     'BB -> N',
                     'BC -> B',
                     'CC -> N',
                     'CN -> C']
        symbols_occurrences = evolve(raw_input, 10)
        self.assertEqual(1588, max(symbols_occurrences.values()) - min(symbols_occurrences.values()))
        symbols_occurrences = evolve(raw_input, 40)
        self.assertEqual(2192039569602, max(symbols_occurrences.values()))
        self.assertEqual(3849876073, min(symbols_occurrences.values()))
        self.assertEqual(2188189693529, max(symbols_occurrences.values()) - min(symbols_occurrences.values()))

    def test_solve_puzzle_1(self):
        raw_input = read_lines('input_day14.txt')
        symbols_occurrences = evolve(raw_input, 10)
        self.assertEqual(4517, max(symbols_occurrences.values()) - min(symbols_occurrences.values()))

    def test_solve_puzzle_2(self):
        raw_input = read_lines('input_day14.txt')
        symbols_occurrences = evolve(raw_input, 40)
        self.assertEqual(4704817645083, max(symbols_occurrences.values()) - min(symbols_occurrences.values()))
