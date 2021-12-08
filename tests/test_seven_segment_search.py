import unittest
from advent_of_code.utilities import read_lines
from collections import Counter, defaultdict

NUMBERS_FOR_SEQUENCE = {
    'cf': '1',
    'abcefg': '0',
    'acdeg': '2',
    'acdfg': '3',
    'bcdf': '4',
    'abdfg': '5',
    'abdefg': '6',
    'acf': '7',
    'abcdefg': '8',
    'abcdfg': '9'
}


def count_easy_digits_in_line(line):
    return len([digit for digit in line.split(' | ')[1].split() if len(digit) in [2, 4, 3, 7]])


def find_first_letter_with_length(letters_occurrences, letter_length):
    return find_all_letters_with_length(letters_occurrences, letter_length)[0]


def find_all_letters_with_length(letters_occurrences, letter_length):
    return [letter_occurrences[0] for letter_occurrences in letters_occurrences if
            letter_occurrences[1] == letter_length]


def calculate_digits_for_length(all_digits):
    length_for_digits = defaultdict(lambda: [])
    for number in all_digits:
        length_for_digits[len(number)].append(number)
    return length_for_digits


def decrypt_number(line):
    all_digits = line.split(' | ')[0].split()
    digits_to_decrypt = line.split(' | ')[1]
    cipher = calculate_cipher(all_digits)
    number_digits = [decrypt_digit(digit_to_decrypt, cipher) for digit_to_decrypt in digits_to_decrypt.split()]
    return int(''.join(number_digits))


def calculate_cipher(all_digits):
    digits_for_length = calculate_digits_for_length(all_digits)
    letters_occurrences = Counter(''.join(all_digits)).items()
    cipher = {
        list(set(digits_for_length[3][0]) - set(digits_for_length[2][0]))[0]: 'a',
        find_first_letter_with_length(letters_occurrences, 9): 'f',
        find_first_letter_with_length(letters_occurrences, 4): 'e',
        find_first_letter_with_length(letters_occurrences, 6): 'b'
    }
    a_and_c = find_all_letters_with_length(letters_occurrences, 8)
    c = next(letter for letter in a_and_c if letter not in cipher.keys())
    cipher[c] = 'c'
    d = next(letter for letter in digits_for_length[4][0] if letter not in cipher.keys())
    cipher[d] = 'd'
    g = next(letter for letter in digits_for_length[7][0] if letter not in cipher.keys())
    cipher[g] = 'g'
    return cipher


def decrypt_digit(digit_to_decrypt, cipher):
    return NUMBERS_FOR_SEQUENCE[''.join(sorted([cipher[letter] for letter in digit_to_decrypt]))]


class SevenSegmentSearchTest(unittest.TestCase):
    def test_puzzle1(self):
        number_of_easy_digits = sum([count_easy_digits_in_line(line) for line in read_lines('input_day8.txt')])
        self.assertEqual(390, number_of_easy_digits)

    def test_puzzle2(self):
        four_digit_output_values = sum([decrypt_number(line) for line in read_lines('input_day8.txt')])
        self.assertEqual(1011785, four_digit_output_values)
