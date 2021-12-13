import unittest
from advent_of_code.utilities import read_lines


class TransparentPaper:

    @classmethod
    def build_from(cls, points):
        return TransparentPaper(points, calculate_max_x(points), calculate_max_y(points))

    def __init__(self, points, max_x, max_y):
        self.points = points
        self.max_x = max_x
        self.max_y = max_y

    def fold_horizontally(self, axes):
        new_max_y = max(axes, abs(self.max_y - axes)) - 1
        new_points = fold_horizontally(self.points, axes, self.max_y)
        return TransparentPaper(new_points, self.max_x, new_max_y)

    def fold_vertically(self, axes):
        new_max_x = max(axes, abs(self.max_x - axes)) - 1
        new_points = fold_vertically(self.points, axes, self.max_x)
        return TransparentPaper(new_points, new_max_x, self.max_y)

    def print(self):
        # print(self.max_x)
        # print(self.max_y)
        for y in range(self.max_y + 1):
            line = ''
            for x in range(self.max_x + 1):
                if (x, y) in self.points:
                    line += '#'
                else:
                    line += '.'
            print(line)


def calculate_max_y(points):
    return max(points, key=lambda p: p[1])[1]


def calculate_max_x(points):
    return max(points, key=lambda p: p[0])[0]


def fold_horizontally(points, axes, max_y):
    upper_points = [p for p in points if p[1] < axes]
    below_points = [p for p in points if p[1] > axes]
    max_below = max(below_points, key=lambda p: p[1])[1]
    new_points = [(p[0], abs(p[1] - max_below)) for p in below_points]
    if max_y // 2 > axes:
        # print('playing with upper points')
        to_add = max_y//2 - axes
        print(upper_points)
        print(to_add)
        upper_points = [(p[0], p[1] + to_add) for p in upper_points]
        print(upper_points)
    if max_y // 2 < axes:
        to_add = axes - max_y//2
        print(to_add)
        new_points = [(p[0], p[1] + to_add) for p in new_points]
    return set(upper_points + new_points)


def fold_vertically(points, axes, max_x):
    left_points = [p for p in points if p[0] < axes]
    right_points = [p for p in points if p[0] > axes]
    max_right = max(right_points, key=lambda p: p[0])[0]
    new_points = [(abs(p[0] - max_right), p[1]) for p in right_points]
    if max_x // 2 > axes:
        to_add = max_x//2 - axes
        left_points = [(p[0] + to_add, p[1]) for p in left_points]
    if max_x // 2 < axes:
        to_add = axes - max_x//2 + 1
        print(to_add)
        new_points = [(p[0] + to_add, p[1]) for p in new_points]
    return set(left_points + new_points)


class TransparentOrigamiTest(unittest.TestCase):
    def test_xyz(self):
        instructions = [
            '6,10',
            '0,14',
            '9,10',
            '0,3',
            '10,4',
            '4,11',
            '6,0',
            '6,12',
            '4,1',
            '0,13',
            '10,12',
            '3,4',
            '3,0',
            '8,4',
            '1,10',
            '2,14',
            '8,10',
            '9,0',
            '',
            'fold along y=7',
            'fold along x=5'
        ]
        instructions_iterator = iter(instructions)
        points = set()
        while True:
            line = next(instructions_iterator)
            if line == '':
                break
            coordinates = [int(c) for c in line.split(',')]
            points.add(tuple(coordinates))
        paper = TransparentPaper.build_from(points) \
            .fold_horizontally(7) \
            .fold_vertically(5)
        paper.print()
        # print(points)
        # for instruction in instructions_iterator:
        #     axes = int(instruction.split('=')[1])
        #     if 'y' in instruction:
        #         points = fold_horizontally(points, axes)
        #     else:
        #         points = fold_vertically(points, axes)
        # print()
        # print(points)
        # max_x = max(points, key=lambda p: p[0])[0]
        # max_y = max(points, key=lambda p: p[1])[1]
        # for y in range(max_y + 1):
        #     line = ''
        #     for x in range(max_x + 1):
        #         if (x, y) in points:
        #             line += '#'
        #         else:
        #             line += '.'
        #     print(line)

    def test_puzzle1(self):
        instructions = read_lines('input_13.txt')
        instructions_iterator = iter(instructions)
        points = set()
        while True:
            line = next(instructions_iterator)
            if line == '':
                break
            coordinates = [int(c) for c in line.split(',')]
            points.add(tuple(coordinates))
        paper = TransparentPaper.build_from(points)
        # paper.print()
        self.assertEqual(820, len(paper.points))
        for instruction in instructions_iterator:
            axes = int(instruction.split('=')[1])
            if 'y' in instruction:
                paper = paper.fold_horizontally(axes)
            else:
                paper = paper.fold_vertically(axes)
        self.assertEqual(-1, len(paper.points))
        # for instruction in instructions_iterator:
        #     axes = int(instruction.split('=')[1])
        #     if 'y' in instruction:
        #         points = fold_horizontally(points, axes)
        #     else:
        #         points = fold_vertically(points, axes)
        # max_x = max(points, key=lambda p: p[0])[0]
        # max_y = max(points, key=lambda p: p[1])[1]
        # for y in range(max_y + 1):
        #     line = ''
        #     for x in range(max_x + 1):
        #         if (x, y) in points:
        #             line += '#'
        #         else:
        #             line += '.'
        #     print(line)
        self.assertEqual(-1, len(points))
