import unittest
from itertools import product

from advent_of_code.utilities import read_lines


def marked_pixels(point):
    return [(point[0] + n[0], point[1] + n[1]) for n in
            [(-1, -1), (0, -1), (1, -1),
             (-1, 0), (0, 0), (1, 0),
             (-1, 1), (0, 1), (1, 1)]]


def parse_image(raw_image):
    image = set()
    for y, row in enumerate(raw_image):
        for x, cell in enumerate(raw_image[y]):
            if cell == '#':
                image.add((x, y))
    return image


def tick(algorithm, image, width, height, offset=4):
    new_image = set()
    for point in product(range(-offset, width + offset), range(-offset, height + offset)):
        binary_number = ''
        for pixel in marked_pixels(point):
            if pixel in image:
                binary_number += '1'
            else:
                binary_number += '0'
        number = int(binary_number, 2)
        if algorithm[number] == '#':
            new_image.add(point)
    return new_image


class TrenchMapTest(unittest.TestCase):
    def test_tick(self):
        algorithm = '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##' \
                    '#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###' \
                    '.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.' \
                    '.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....' \
                    '.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..' \
                    '...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....' \
                    '..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#'

        raw_input_image = ['#..#.',
                           '#....',
                           '##..#',
                           '..#..',
                           '..###']
        height = len(raw_input_image)
        width = len(raw_input_image[0])
        image = parse_image(raw_input_image)
        image = tick(algorithm, image, width, height)
        image = tick(algorithm, image, width, height)
        self.assertEqual(35, len(image))
        offset = 2
        for _ in range(24):
            offset += 4
            image = tick(algorithm, image, width, height, offset)
            offset -= 2
            image = tick(algorithm, image, width, height, offset)
        self.assertEqual(3351, len(image))


    def test_puzzles(self):
        puzzle_input = read_lines('input_day20.txt')
        algorithm = puzzle_input[0]
        raw_input_image = puzzle_input[2:]
        height = len(raw_input_image)
        width = len(raw_input_image[0])
        image = parse_image(raw_input_image)
        self.assertEqual(4994, len(image))
        offset = 4
        image = tick(algorithm, image, width, height, offset)
        offset -= 2
        image = tick(algorithm, image, width, height, offset)
        self.assertEqual(5229, len(image))
        for _ in range(24):
            offset += 4
            image = tick(algorithm, image, width, height, offset)
            offset -= 2
            image = tick(algorithm, image, width, height, offset)
        self.assertEqual(17009, len(image))
