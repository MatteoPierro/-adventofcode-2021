import unittest

from advent_of_code.utilities import read_lines
from functools import reduce


def diagnostic_sum(current, number):
    return list(map(sum, zip(current, map(int, number))))


def convert_to_int(binary):
    return int(''.join(map(str, binary)), 2)


def power_consumption(report):
    number_length = len(report)
    binary_gamma_rate = list(map(lambda x: 1 if x > number_length / 2 else 0,
                                 reduce(diagnostic_sum, report, [0] * number_length)))
    gamma_rate = convert_to_int(binary_gamma_rate)
    binary_epsilon_rate = list(map(lambda d: d ^ 1, binary_gamma_rate))
    epsilon_rate = convert_to_int(binary_epsilon_rate)
    return gamma_rate * epsilon_rate


class BinaryDiagnosticTest(unittest.TestCase):
    def test_binary_diagnostic(self):
        report = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010',
                  '01010']
        self.assertEqual(198, power_consumption(report))

    def test_puzzle_1(self):
        report = read_lines('input_day3.txt')
        self.assertEqual(4160394, power_consumption(report))
