import unittest
from collections import defaultdict
from advent_of_code.utilities import read_lines


def parse_connection(raw_connection):
    return raw_connection.split('-')


def calculate_adjacent_matrix(raw_connections):
    connections = [parse_connection(c) for c in raw_connections]
    adjacency_matrix = defaultdict(lambda: [])
    for c in connections:
        adjacency_matrix[c[0]].append(c[1])
        adjacency_matrix[c[1]].append(c[0])
    return adjacency_matrix


def find_paths(current_vertex, matrix, current_path, all_paths):
    if current_vertex == 'end':
        all_paths.append(current_path)
        return

    for v in matrix[current_vertex]:
        if v.islower() and v in current_path:
            continue
        new_path = list(current_path)
        new_path.append(v)
        find_paths(v, matrix, new_path, all_paths)


def find_number_of_paths(raw_connections):
    adjacency_matrix = calculate_adjacent_matrix(raw_connections)
    all_paths = []
    find_paths('start', adjacency_matrix, ['start'], all_paths)
    return len(all_paths)


class PassagePathingTest(unittest.TestCase):
    def test_find_number_of_paths(self):
        raw_connections = [
            'start-A',
            'start-b',
            'A-c',
            'A-b',
            'b-d',
            'A-end',
            'b-end'
        ]
        self.assertEqual(10, find_number_of_paths(raw_connections))

    def test_puzzle_1(self):
        raw_connections = read_lines('input_day12.txt')
        self.assertEqual(3738, find_number_of_paths(raw_connections))
