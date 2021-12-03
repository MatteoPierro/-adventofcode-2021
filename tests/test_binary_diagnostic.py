import unittest

from advent_of_code.utilities import read_lines
from functools import reduce


def diagnostic_sum(current, number):
    return list(map(sum, zip(current, map(int, number))))


def convert_to_int(binary):
    return int(''.join(map(str, binary)), 2)


def power_consumption(report):
    report_length = len(report)
    binary_gamma_rate = list(map(lambda x: 1 if x > report_length / 2 else 0,
                                 reduce(diagnostic_sum, report, [0] * len(report[0]))))
    gamma_rate = convert_to_int(binary_gamma_rate)
    binary_epsilon_rate = list(map(lambda d: d ^ 1, binary_gamma_rate))
    epsilon_rate = convert_to_int(binary_epsilon_rate)
    return gamma_rate * epsilon_rate


def select_oxygen(common, digit):
    return common == digit


def select_co2(common, digit):
    return not select_oxygen(common, digit)


def oxygen_generator_rating(report):
    return rating(report, 0, select_oxygen)


def co2_scrubber_rating(report):
    return rating(report, 0, select_co2)


def rating(report, index, selector):
    if len(report) == 1:
        return report[0]
    report_length = len(report)
    common = most_common_digit(sum(map(lambda number: int(number[index]), report)), report_length / 2)
    remaining_common = list(filter(lambda number: selector(common, int(number[index])), report))
    return rating(remaining_common, index + 1, selector)


def most_common_digit(ones, half):
    return 0 if ones < half else 1


class BinaryDiagnosticTest(unittest.TestCase):
    def test_binary_diagnostic(self):
        report = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010',
                  '01010']
        self.assertEqual(198, power_consumption(report))

    def test_puzzle_1(self):
        report = read_lines('input_day3.txt')
        self.assertEqual(4160394, power_consumption(report))

    def test_life_supporting_rate(self):
        report = ['00100', '11110', '10110', '10111', '10101', '01111', '00111', '11100', '10000', '11001', '00010',
                  '01010']
        oxygen = oxygen_generator_rating(report)
        self.assertEqual('10111', oxygen)
        co2 = co2_scrubber_rating(report)
        self.assertEqual('01010', co2)

    def test_puzzle_2(self):
        report = read_lines('input_day3.txt')
        oxygen = convert_to_int(oxygen_generator_rating(report))
        co2 = convert_to_int(co2_scrubber_rating(report))
        self.assertEqual(4125600, oxygen * co2)
