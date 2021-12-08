import unittest
from advent_of_code.utilities import read_lines


def count_easy_digits_in_line(line):
    return len([digit for digit in line.split(' | ')[1].split() if len(digit) in [2, 4, 3, 7]])


class SevenSegmentSearchTest(unittest.TestCase):
    def test_puzzle1(self):
        number_of_easy_digits = sum([count_easy_digits_in_line(line) for line in read_lines('input_day8.txt')])
        self.assertEqual(390, number_of_easy_digits)
