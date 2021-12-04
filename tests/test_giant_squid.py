import unittest

from advent_of_code.utilities import read_lines


class Board:
    def __init__(self, board):
        self.board = list(board)

    def __getitem__(self, item):
        return self.board[item]

    def extracted_number(self, number):
        for row_index in range(len(self.board)):
            self.board[row_index] = ['X' if tile == number else tile for tile in self.board[row_index]]

    def has_won(self):
        for index in range(5):
            if is_completed(self.board[index]):
                return True
            column = [row[index] for row in self.board]
            if is_completed(column):
                return True
        return False

    def sum(self):
        s = 0
        for row in self.board:
            for tile in row:
                if tile != 'X':
                    s += tile
        return s


def is_completed(line):
    return all(tile == 'X' for tile in line)


def score(boards, drawn_numbers):
    for number in drawn_numbers:
        for board in boards:
            board.extracted_number(number)
            if board.has_won():
                return number * board.sum()
    raise 'No Winner something went wrong!!!'


def parse_drawn_numbers(l):
    return list(map(int, l.split(',')))


def parse_row(row):
    return list(map(int, row.split()))


class GiantSquidTest(unittest.TestCase):
    def test_board(self):
        board = Board([
            [14, 21, 17, 24, 4],
            [10, 16, 15, 9, 19],
            [18, 8, 23, 26, 20],
            [22, 11, 13, 6, 5],
            [2, 0, 12, 3, 7]
        ])
        board.extracted_number(7)
        self.assertEqual([2, 0, 12, 3, 'X'], board[-1])
        board.extracted_number(4)
        self.assertEqual([14, 21, 17, 24, 'X'], board[0])
        for n in [9, 5, 11, 17, 23, 2, 0, 14, 21, 24]:
            board.extracted_number(n)
        self.assertTrue(board.has_won())
        self.assertEqual(188, board.sum())

    def test_winning_board_on_columns(self):
        new_board = Board([
            [14, 21, 17, 24, 4],
            [10, 16, 15, 9, 19],
            [18, 8, 23, 26, 20],
            [22, 11, 13, 6, 5],
            [2, 0, 12, 3, 7]
        ])
        for n in [14, 10, 18, 22, 2]:
            new_board.extracted_number(n)
        self.assertTrue(new_board.has_won())

    def test_score(self):
        boards = [Board([
            [14, 21, 17, 24, 4],
            [10, 16, 15, 9, 19],
            [18, 8, 23, 26, 20],
            [22, 11, 13, 6, 5],
            [2, 0, 12, 3, 7]
        ])]
        drawn_numbers = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26,
                         1]
        self.assertEqual(4512, score(boards, drawn_numbers))

    def test_puzzle1(self):
        puzzle_input = read_lines('./input_day4.txt')
        drawn_numbers = parse_drawn_numbers(puzzle_input[0])
        boards = []
        for index in range(2, len(puzzle_input), 6):
            raw_board = [parse_row(row) for row in puzzle_input[index: index + 5]]
            boards.append(Board(raw_board))
        self.assertEqual(29440, score(boards, drawn_numbers))
