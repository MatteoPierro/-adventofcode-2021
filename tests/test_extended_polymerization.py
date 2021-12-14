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


def evolve(polymer_template, rules, times):
    for _ in range(times):
        new_polymer_template = []
        for adjacent in zip(polymer_template, polymer_template[1:]):
            to_insert = rules[adjacent]
            new_polymer_template.append(adjacent[0])
            new_polymer_template.append(to_insert)
        new_polymer_template.append(polymer_template[-1])
        polymer_template = new_polymer_template
    return polymer_template


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

        polymer_template, rules = parse_input(raw_input)
        polymer_template = evolve(polymer_template, rules, 4)
        self.assertEqual('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB', ''.join(polymer_template))

        polymer_template, rules = parse_input(raw_input)
        polymer_template = evolve(polymer_template, rules, 10)
        values = sorted(Counter(polymer_template).values())
        self.assertEqual(1588, values[-1] - values[0])

    def test_solve_puzzle_1(self):
        raw_input = read_lines('input_day14.txt')
        polymer_template, rules = parse_input(raw_input)
        polymer_template = evolve(polymer_template, rules, 10)
        values = sorted(Counter(polymer_template).values())
        self.assertEqual(4517, values[-1] - values[0])