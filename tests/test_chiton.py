import unittest
from queue import PriorityQueue

from advent_of_code.utilities import read_lines

from collections import defaultdict
from itertools import product
import numpy as np


# https://stackabuse.com/dijkstras-algorithm-in-python/
class UnidirectionalGraph:
    def __init__(self):
        self.edges = defaultdict(lambda: {})

    def add_edge(self, v1, v2, weight):
        self.edges[v1][v2] = weight

    def dijkstra(self, start_vertex, end=None):
        distances = {v: float('inf') for v in self.edges.keys()}
        distances[start_vertex] = 0

        queue = PriorityQueue()
        queue.put((0, start_vertex))
        visited = set()

        while not queue.empty():
            (distance_to_current_vertex, current_vertex) = queue.get()

            for neighbor in self.edges[current_vertex].keys():
                if neighbor in visited:
                    continue
                distance = self.edges[current_vertex][neighbor]
                old_cost = distances[neighbor]
                new_cost = distance_to_current_vertex + distance
                if new_cost < old_cost:
                    queue.put((new_cost, neighbor))
                    distances[neighbor] = new_cost

            visited.add(current_vertex)
            if current_vertex == end:
                return distances[current_vertex]
        return distances


def find_shortest_path_cost(risk_map):
    height = len(risk_map)
    width = len(risk_map[0])
    g = UnidirectionalGraph()
    for x, y in product(range(width), range(height)):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n = (x + dx, y + dy)
            if 0 <= n[0] < width and 0 <= n[1] < height:
                g.add_edge((x, y), n, risk_map[n[1]][n[0]])
    return g.dijkstra((0, 0), end=(width - 1, height - 1))


def parse_row(row):
    return [int(v) for v in row]


def create_bigger_risk_level_map(risk_level_map):
    lx = len(risk_level_map[0])
    ly = len(risk_level_map)
    small_matrix = np.array(risk_level_map)
    to_add = np.array([list(range(5)), list(range(1, 6)),
                       list(range(2, 7)), list(range(3, 8)), list(range(4, 9))])
    total_matrix = np.kron(np.ones((5, 5)), small_matrix) + np.kron(to_add, np.ones((lx, ly)))
    total_matrix[total_matrix > 9] -= 9
    return total_matrix


class ChitonTest(unittest.TestCase):
    def test_find_shortest_path_cost(self):
        raw_risk_map = [
            '1163751742',
            '1381373672',
            '2136511328',
            '3694931569',
            '7463417111',
            '1319128137',
            '1359912421',
            '3125421639',
            '1293138521',
            '2311944581'
        ]
        risk_map = [parse_row(row) for row in raw_risk_map]
        self.assertEqual(40, find_shortest_path_cost(risk_map))
        self.assertEqual(315, find_shortest_path_cost(create_bigger_risk_level_map(risk_map)))

    def test_puzzles(self):
        raw_risk_map = read_lines('input_day15.txt')
        risk_map = [parse_row(row) for row in raw_risk_map]
        self.assertEqual(363, find_shortest_path_cost(risk_map))
        self.assertEqual(2835, find_shortest_path_cost(create_bigger_risk_level_map(risk_map)))
