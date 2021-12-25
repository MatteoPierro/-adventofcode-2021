import unittest
from advent_of_code.utilities import read_lines


class SeaCucumberTest(unittest.TestCase):
    def test_puzzle(self):
        raw_initial_state = read_lines('input_day25.txt')

        initial_state = {
            '>': set(),
            'v': set()
        }
        width = len(raw_initial_state[0])
        height = len(raw_initial_state)
        for y, row in enumerate(raw_initial_state):
            for x, cell in enumerate(row):
                if cell == '>':
                    initial_state['>'].add((x, y))
                if cell == 'v':
                    initial_state['v'].add((x, y))
        current_state = initial_state
        steps = 0
        while True:
            new_state = {
                '>': set(),
                'v': set()
            }
            for (x, y) in current_state['>']:
                new_x = (x + 1) % width
                if (new_x, y) not in current_state['>'] and (new_x, y) not in current_state['v']:
                    new_state['>'].add((new_x, y))
                else:
                    new_state['>'].add((x, y))
            for x, y in current_state['v']:
                new_y = (y + 1) % height
                if (x, new_y) not in new_state['>'] and (x, new_y) not in current_state['v']:
                    new_state['v'].add((x, new_y))
                else:
                    new_state['v'].add((x, y))
            steps += 1
            if current_state == new_state:
                break
            current_state = new_state
        self.assertEqual(498, steps)
