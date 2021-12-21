import unittest
from collections import Counter

from advent_of_code.utilities import read_blocks


def parse_input(raw_input):
    scanners = []
    for raw_scanner in raw_input:
        scanner = []
        for scan in raw_scanner[1:]:
            x, y, z = scan.split(',')
            scanner.append([int(x), int(y), int(z)])
        scanners.append(Scanner(scanner))
    scanners[0].beacons_aligned_positions = scanners[0].beacons_original_positions
    scanners[0].absolute_position = (0, 0, 0)
    return scanners


class Scanner:
    def __init__(self, beacons_original_positions):
        self.beacons_original_positions = beacons_original_positions
        self.beacons_aligned_positions = None
        self.absolute_position = None

    def beacons_positions(self):
        return [add(self.absolute_position, beacon) for beacon in self.beacons_aligned_positions]


def add(point1, point2):
    return [x1 + x2 for (x1, x2) in zip(point1, point2)]


def difference(point1, point2):
    return [x1 - x2 for (x1, x2) in zip(point1, point2)]


def find_scanners_positions(scanners):
    if all(scanner.absolute_position is not None for scanner in scanners):
        return
    already_placed_scanners = [scanner for scanner in scanners if scanner.absolute_position is not None]
    for placed_scanner in already_placed_scanners:
        scanner_to_place = [scanner for scanner in scanners if scanner.absolute_position is None]
        for scanner in scanner_to_place:
            find_scanner_origin(placed_scanner, scanner)
    return find_scanners_positions(scanners)


def find_scanner_origin(already_placed_scanner, scanner):
    all_rotated_scanners = get_all_rotated_scanners(scanner.beacons_original_positions)
    for rotated_scanner in all_rotated_scanners:
        candidate_origin = []
        for point0 in already_placed_scanner.beacons_aligned_positions:
            for point in rotated_scanner:
                candidate_origin.append(tuple(difference(point0, point)))
        all_distances = Counter(candidate_origin)
        origin = max(all_distances, key=all_distances.get)
        if all_distances[origin] >= 12:
            scanner.absolute_position = add(already_placed_scanner.absolute_position, origin)
            scanner.beacons_aligned_positions = rotated_scanner
            return


def get_all_rotated_scanners(scanner):
    rotations = []
    for beacon in scanner:
        orientations = get_orientations(beacon)
        for index, o in enumerate(orientations):
            if len(rotations) < index + 1:
                rotations.append([])
            rotations[index].append(o)
    return rotations


def get_orientations(point):
    x, y, z = point
    for xi, yi, zi in get_z_orientations(x, y, z):
        yield from get_rotations(xi, yi, zi)


def get_z_orientations(x, y, z):
    return [
        (x, y, z),
        (x, z, -y),
        (x, -y, -z),
        (x, -z, y),
        (-z, y, x),
        (z, y, -x),
    ]


def get_rotations(x, y, z):
    return [
        (x, y, z),
        (-y, x, z),
        (-x, -y, z),
        (y, -x, z),
    ]


def find_unique_beacons(scanners):
    beacons = set()
    for scanner in scanners:
        for b in scanner.beacons_positions():
            beacons.add(tuple(b))
    unique_beacons = len(beacons)
    return unique_beacons


def calculate_max_distance(scanners):
    max_distance = 0
    for s1 in scanners:
        for s2 in scanners:
            x, y, z = difference(s1.absolute_position, s2.absolute_position)
            distance = abs(x) + abs(y) + abs(z)
            if distance > max_distance:
                max_distance = distance
    return max_distance


class BeaconScannerTest(unittest.TestCase):
    def test_small_input(self):
        raw_scanners = read_blocks('input_day19_test.txt')
        scanners = parse_input(raw_scanners)
        find_scanners_positions(scanners)
        self.assertEqual([68, -1246, -43], scanners[1].absolute_position)
        self.assertEqual([-20, -1133, 1061], scanners[4].absolute_position)
        self.assertEqual([-92, -2380, -20], scanners[3].absolute_position)
        self.assertEqual([1105, -1205, 1229], scanners[2].absolute_position)
        self.assertEqual(79, find_unique_beacons(scanners))
        self.assertEqual(3621, calculate_max_distance(scanners))

    def test_puzzles(self):
        raw_scanners = read_blocks('input_day19.txt')
        scanners = parse_input(raw_scanners)
        find_scanners_positions(scanners)
        self.assertEqual(376, find_unique_beacons(scanners))
        self.assertEqual(10772, calculate_max_distance(scanners))
