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


def evolve_adjacent(adjacent, rules, current_step, number_of_steps, memo):
    if current_step == number_of_steps:
        memo[(adjacent, current_step)] = Counter(adjacent[0])
    if (adjacent, current_step) in memo.keys():
        return memo[(adjacent, current_step)]

    element_to_insert = rules[adjacent]
    left = (adjacent[0], element_to_insert)
    right = (element_to_insert, adjacent[1])
    left_number_of_symbols = evolve_adjacent(left, rules, current_step + 1, number_of_steps, memo)
    right_number_of_symbols = evolve_adjacent(right, rules, current_step + 1, number_of_steps, memo)
    memo[(adjacent, current_step)] = left_number_of_symbols + right_number_of_symbols
    return memo[(adjacent, current_step)]


class ExtendedPolymerizationTest(unittest.TestCase):
    def test_evolve_adjacent(self):
        raw_input = ['NNCB',
                     '',
                     'CH -> B',  # CH -> CBH
                     'HH -> N',  # HH -> HNH
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
        symbols = Counter(polymer_template)
        # polymer_template = ['N', 'N']
        memo = {}
        for adjacent in zip(polymer_template, polymer_template[1:]):
            symbols = symbols + evolve_adjacent(adjacent, rules, 0, 40, memo)
        self.assertEqual(2192039569602, max(symbols.values()))
        self.assertEqual(3849876073, min(symbols.values()))
        self.assertEqual(2188189693529, max(symbols.values()) - min(symbols.values()))

    def test_evolve(self):
        raw_input = ['NNCB',
                     '',
                     'CH -> B',  # CH -> CBH
                     'HH -> N',  # HH -> HNH
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
        symbols = Counter(polymer_template)
        memo = {}
        for adjacent in zip(polymer_template, polymer_template[1:]):
            symbols = symbols + evolve_adjacent(adjacent, rules, 0, 10, memo)
        symbols += Counter([polymer_template[-1], polymer_template[-1]])
        self.assertEqual(4517, max(symbols.values()) - min(symbols.values()))

    def test_solve_puzzle_2(self):
        raw_input = read_lines('input_day14.txt')
        polymer_template, rules = parse_input(raw_input)
        symbols = Counter(polymer_template)
        memo = {}
        for adjacent in zip(polymer_template, polymer_template[1:]):
            symbols = symbols + evolve_adjacent(adjacent, rules, 0, 40, memo)
        symbols += Counter([polymer_template[-1], polymer_template[-1]])
        self.assertEqual(4704817645083, max(symbols.values()) - min(symbols.values()))
