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


def evolve_adjacent(adjacent, rules, number_of_steps, memo):
    if number_of_steps == 0:
        memo[(adjacent, number_of_steps)] = Counter(adjacent[0])
    if (adjacent, number_of_steps) in memo.keys():
        return memo[(adjacent, number_of_steps)]

    element_to_insert = rules[adjacent]
    left = (adjacent[0], element_to_insert)
    right = (element_to_insert, adjacent[1])
    left_number_of_symbols = evolve_adjacent(left, rules, number_of_steps - 1, memo)
    right_number_of_symbols = evolve_adjacent(right, rules, number_of_steps - 1, memo)
    memo[(adjacent, number_of_steps)] = left_number_of_symbols + right_number_of_symbols
    return memo[(adjacent, number_of_steps)]


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
        symbols = Counter(polymer_template)
        memo = {}
        for adjacent in zip(polymer_template, polymer_template[1:]):
            symbols = symbols + evolve_adjacent(adjacent, rules, 10, memo)
        symbols += Counter([polymer_template[-1], polymer_template[-1]])
        self.assertEqual(4517, max(symbols.values()) - min(symbols.values()))

    def test_evolve_adjacent(self):
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
        symbols = Counter(polymer_template)
        memo = {}
        for adjacent in zip(polymer_template, polymer_template[1:]):
            symbols = symbols + evolve_adjacent(adjacent, rules, 40, memo)
        self.assertEqual(2192039569602, max(symbols.values()))
        self.assertEqual(3849876073, min(symbols.values()))
        self.assertEqual(2188189693529, max(symbols.values()) - min(symbols.values()))

    def test_solve_puzzle_2(self):
        raw_input = read_lines('input_day14.txt')
        polymer_template, rules = parse_input(raw_input)
        symbols = Counter(polymer_template)
        memo = {}
        for adjacent in zip(polymer_template, polymer_template[1:]):
            symbols = symbols + evolve_adjacent(adjacent, rules, 40, memo)
        symbols += Counter([polymer_template[-1], polymer_template[-1]])
        self.assertEqual(4704817645083, max(symbols.values()) - min(symbols.values()))
