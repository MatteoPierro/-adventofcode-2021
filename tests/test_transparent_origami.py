import unittest
from advent_of_code.utilities import read_lines

X_COMPONENT = 0
Y_COMPONENT = 1


class TransparentPaper:

    @classmethod
    def build_from(cls, points):
        return TransparentPaper(points, calculate_max(points, X_COMPONENT), calculate_max(points, Y_COMPONENT))

    def __init__(self, points, max_x, max_y):
        self.points = points
        self.max_x = max_x
        self.max_y = max_y

    def execute_instruction(self, instruction):
        axes = int(instruction.split('=')[1])
        if 'y' in instruction:
            paper = self.fold_horizontally(axes)
        else:
            paper = self.fold_vertically(axes)
        return paper

    def fold_horizontally(self, axes):
        new_max_y = max(axes, abs(self.max_y - axes)) - 1
        new_points = fold_horizontally(self.points, axes, self.max_y, new_max_y)
        return TransparentPaper(new_points, self.max_x, new_max_y)

    def fold_vertically(self, axes):
        new_max_x = max(axes, abs(self.max_x - axes)) - 1
        new_points = fold_vertically(self.points, axes, self.max_x, new_max_x)
        return TransparentPaper(new_points, new_max_x, self.max_y)

    def __str__(self):
        lines = []
        for y in range(self.max_y + 1):
            line = ''
            for x in range(self.max_x + 1):
                if (x, y) in self.points:
                    line += '#'
                else:
                    line += '.'
            lines.append(line)
        return '\n'.join(lines)


def calculate_max(points, component):
    return max(points, key=lambda p: p[component])[component]


def fold_horizontally(points, axes, old_max_y, new_max_y):
    upper_points = [p for p in points if p[1] < axes]
    below_points = [p for p in points if p[1] > axes]
    new_points = [(p[0], abs(p[1] - old_max_y)) for p in below_points]
    if old_max_y // 2 > axes:
        to_add = new_max_y - axes + 1
        upper_points = [(p[0], p[1] + to_add) for p in upper_points]
    if old_max_y // 2 < axes:
        to_add = new_max_y - (old_max_y - axes) + 1
        new_points = [(p[0], p[1] + to_add) for p in new_points]
    return set(upper_points + new_points)


def fold_vertically(points, axes, old_max_x, new_max_x):
    left_points = [p for p in points if p[0] < axes]
    right_points = [p for p in points if p[0] > axes]
    new_points = [(abs(p[0] - old_max_x), p[1]) for p in right_points]
    if old_max_x // 2 > axes:
        to_add = new_max_x - axes + 1
        left_points = [(p[0] + to_add, p[1]) for p in left_points]
    if old_max_x // 2 < axes:
        to_add = new_max_x - (old_max_x - axes) + 1
        new_points = [(p[0] + to_add, p[1]) for p in new_points]
    return set(left_points + new_points)


def parse_input(raw_input):
    instructions_iterator = iter(raw_input)
    points = set()
    while True:
        line = next(instructions_iterator)
        if line == '':
            break
        coordinates = [int(c) for c in line.split(',')]
        points.add(tuple(coordinates))
    paper = TransparentPaper.build_from(points)
    return instructions_iterator, paper


def execute_instructions(instructions, paper):
    for instruction in instructions:
        paper = paper.execute_instruction(instruction)
    return paper


class TransparentOrigamiTest(unittest.TestCase):
    def test_fold(self):
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
        instructions, paper = parse_input(instructions)
        instruction = next(instructions)
        paper = paper.execute_instruction(instruction)
        self.assertEqual(17, len(paper.points))
        paper = execute_instructions(instructions, paper)
        expected_paper = '#####\n' \
                         '#...#\n' \
                         '#...#\n' \
                         '#...#\n' \
                         '#####\n' \
                         '.....\n' \
                         '.....'
        self.assertEqual(expected_paper, str(paper))

    def test_puzzle(self):
        raw_input = read_lines('input_day13.txt')
        instructions, paper = parse_input(raw_input)
        instruction = next(instructions)
        paper = paper.execute_instruction(instruction)
        self.assertEqual(682, len(paper.points))
        paper = execute_instructions(instructions, paper)
        expected_paper = '####..##...##..#..#.###..####.#..#.####.\n' \
                         '#....#..#.#..#.#..#.#..#....#.#..#.#....\n' \
                         '###..#..#.#....#..#.#..#...#..####.###..\n' \
                         '#....####.#.##.#..#.###...#...#..#.#....\n' \
                         '#....#..#.#..#.#..#.#.#..#....#..#.#....\n' \
                         '#....#..#..###..##..#..#.####.#..#.####.'
        self.assertEqual(expected_paper, str(paper))
