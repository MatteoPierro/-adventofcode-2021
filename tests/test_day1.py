import unittest

from advent_of_code.utilities import read_lines


def increased_window_depth_measurements(depth_measurements):
    window_depth_measurements = list(
        map(sum, zip(depth_measurements, depth_measurements[1:], depth_measurements[2:])))
    return increased_depth_measurements(window_depth_measurements)


def increased_depth_measurements(depth_measurements):
    return len(list(filter(lambda t: t[1] > t[0], zip(depth_measurements, depth_measurements[1:]))))


class Day1Test(unittest.TestCase):
    def test_increased_depth_measurements(self):
        depth_measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        self.assertEqual(7, increased_depth_measurements(depth_measurements))

    def test_solution_puzzle1(self):
        depth_measurements = list(map(int, read_lines('input_day1.txt')))
        self.assertEqual(1616, increased_depth_measurements(depth_measurements))

    def test_increased_window_depth_measurements(self):
        depth_measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        self.assertEqual(5, increased_window_depth_measurements(depth_measurements))

    def test_solution_puzzle2(self):
        depth_measurements = list(map(int, read_lines('input_day1.txt')))
        self.assertEqual(1645, increased_window_depth_measurements(depth_measurements))


if __name__ == '__main__':
    unittest.main()
