import unittest
from advent_of_code.utilities import read_lines

PARENTHESIS = {
    '}': '{',
    ']': '[',
    ')': '(',
    '>': '<'
}

SCORE_MAP = {
    '}': 1197,
    ']': 57,
    ')': 3,
    '>': 25137
}


def find_find_first_illegal_character(line, opens):
    if not line:
        return None
    char = line.pop(0)
    if char in PARENTHESIS.values():
        opens.append(char)
    else:
        last_opened = opens.pop()
        if last_opened != PARENTHESIS[char]:
            return char
    return find_find_first_illegal_character(line, opens)


def find_scores_first_invalid_chars(lines):
    first_invalid_chars = [find_find_first_illegal_character(list(line), []) for line in lines]
    score = sum([SCORE_MAP[c] for c in first_invalid_chars if c in SCORE_MAP.keys()])
    return score


class SyntaxScoringTest(unittest.TestCase):
    def test_find_first_illegal_character(self):
        self.assertEqual(']', find_find_first_illegal_character(list('(]'), []))
        self.assertEqual(None, find_find_first_illegal_character(list('()'), []))
        self.assertEqual('}', find_find_first_illegal_character(list('{([(<{}[<>[]}>{[]{[(<()>'), []))

    def test_find_scores_first_invalid_chars(self):
        lines = [
            '[({(<(())[]>[[{[]{<()<>>',
            '[(()[<>])]({[<{<<[]>>(',
            '{([(<{}[<>[]}>{[]{[(<()>',
            '(((({<>}<{<{<>}{[]{[]{}',
            '[[<[([]))<([[{}[[()]]]',
            '[{[{({}]{}}([{[{{{}}([]',
            '{<[[]]>}<{[{[{[]{()[[[]',
            '[<(<(<(<{}))><([]([]()',
            '<{([([[(<>()){}]>(<<{{',
            '<{([{{}}[<[[[<>{}]]]>[]]']
        self.assertEqual(26397, find_scores_first_invalid_chars(lines))

    def test_puzzle_1(self):
        lines = read_lines('input_day10.txt')
        self.assertEqual(370407, find_scores_first_invalid_chars(lines))
