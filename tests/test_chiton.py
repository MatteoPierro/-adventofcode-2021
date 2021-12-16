import unittest
from queue import PriorityQueue

from advent_of_code.utilities import read_lines

from collections import defaultdict
from itertools import product


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


def find_shortest_path_cost(raw_risk_map):
    risk_map = [parse_row(row) for row in raw_risk_map]
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
        self.assertEqual(40, find_shortest_path_cost(raw_risk_map))

    def test_puzzle1(self):
        raw_risk_map = read_lines('input_day15.txt')
        self.assertEqual(363, find_shortest_path_cost(raw_risk_map))
