import unittest
import collections

from advent_of_code.utilities import read_lines


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def all_points(self):
        if self.is_vertical():
            start = min(self.start[1], self.end[1])
            end = max(self.start[1], self.end[1])
            return [(self.start[0], i) for i in range(start, end + 1)]
        if self.is_horizontal():
            start = min(self.start[0], self.end[0])
            end = max(self.start[0], self.end[0])
            return [(i, self.start[1]) for i in range(start, end + 1)]
        raise 'Not implemented yet!'

    def is_vertical_or_horizontal(self):
        return self.is_vertical() or self.is_horizontal()

    def is_vertical(self):
        return self.start[0] == self.end[0]

    def is_horizontal(self):
        return self.start[1] == self.end[1]

    def __str__(self):
        return f"{self.start} -> {self.end}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


def number_of_points_with_two_or_more_occurrences(lines):
    points = [point for line in horizontal_and_vertical_lines(lines) for point in line.all_points()]
    point_occurrences = collections.Counter(points)
    return len([elem for elem in point_occurrences.items() if elem[1] > 1])


def horizontal_and_vertical_lines(lines):
    return [line for line in lines if line.is_vertical_or_horizontal()]


def parse_line(raw_line):
    row_points = raw_line.split(' -> ')
    return Line(parse_point(row_points[0]), parse_point(row_points[1]))


def parse_point(raw_point):
    coordinates = raw_point.split(',')
    return int(coordinates[0]), int(coordinates[1])


class HydrothermalVentureTest(unittest.TestCase):
    def test_points_in_line(self):
        self.assertEqual([(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)], Line((0, 9), (5, 9)).all_points())
        self.assertEqual([(7, 0), (7, 1), (7, 2), (7, 3), (7, 4)], Line((7, 4), (7, 0)).all_points())

    def test_filter_horizontal_and_vertical_lines(self):
        lines = [Line((0, 9), (5, 9)),
                 Line((8, 0), (0, 8)),
                 Line((9, 4), (3, 4)),
                 Line((2, 2), (2, 1)),
                 Line((7, 0), (7, 4)),
                 Line((6, 4), (2, 0)),
                 Line((0, 9), (2, 9)),
                 Line((3, 4), (1, 4)),
                 Line((0, 0), (8, 8)),
                 Line((5, 5), (8, 2))]
        self.assertEqual([Line((0, 9), (5, 9)), Line((9, 4), (3, 4)), Line((2, 2), (2, 1)), Line((7, 0), (7, 4)),
                          Line((0, 9), (2, 9)), Line((3, 4), (1, 4))], horizontal_and_vertical_lines(lines))
        self.assertEqual(5, number_of_points_with_two_or_more_occurrences(lines))

    def test_parse_line(self):
        self.assertEqual(Line((2, 2), (2, 1)), parse_line('2,2 -> 2,1'))

    def test_puzzle1(self):
        raw_lines = read_lines('input_day5.txt')
        lines = [parse_line(line) for line in raw_lines]
        self.assertEqual(7085, number_of_points_with_two_or_more_occurrences(lines))