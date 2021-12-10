import unittest
from advent_of_code.utilities import read_lines

PARENTHESIS = {
    '}': '{',
    ']': '[',
    ')': '(',
    '>': '<'
}

CLOSE_PARENTHESIS_FOR_OPEN = {
    '{': '}',
    '[': ']',
    '(': ')',
    '<': '>'
}

SCORE_MAP = {
    '}': 1197,
    ']': 57,
    ')': 3,
    '>': 25137
}

ILLEGAL_SCORE_MAP = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
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


def find_remaining_to_close(raw_line):
    line = list(raw_line)
    remaining_opens = []
    illegal = find_find_first_illegal_character(line, remaining_opens)
    if illegal is not None:
        return None
    return [CLOSE_PARENTHESIS_FOR_OPEN[p] for p in reversed(remaining_opens)]


def calculate_score_remaining_to_close(remaining_to_close):
    score = 0
    for p in remaining_to_close:
        score *= 5
        score += ILLEGAL_SCORE_MAP[p]
    return score


def find_middle_score_of_remaining_to_close(lines):
    scores = []
    for line in lines:
        remaining_to_close = find_remaining_to_close(line)
        if remaining_to_close is None:
            continue
        scores.append(calculate_score_remaining_to_close(remaining_to_close))
    scores.sort()
    middle_index = int((len(scores) - 1) / 2)
    return scores[middle_index]


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

    def test_find_remaining_to_close(self):
        self.assertEqual(list('}}]])})]'), find_remaining_to_close('[({(<(())[]>[[{[]{<()<>>'))
        self.assertEqual(list(')}>]})'), find_remaining_to_close('[(()[<>])]({[<{<<[]>>('))
        self.assertEqual(list('}}>}>))))'), find_remaining_to_close('(((({<>}<{<{<>}{[]{[]{}'))
        self.assertEqual(list(']]}}]}]}>'), find_remaining_to_close('{<[[]]>}<{[{[{[]{()[[[]'))
        self.assertEqual(list('])}>'), find_remaining_to_close('<{([{{}}[<[[[<>{}]]]>[]]'))

    def test_calculate_score_remaining_to_close(self):
        self.assertEqual(294, calculate_score_remaining_to_close(list('])}>')))
        self.assertEqual(288957, calculate_score_remaining_to_close(list('}}]])})]')))
        self.assertEqual(5566, calculate_score_remaining_to_close(list(')}>]})')))
        self.assertEqual(1480781, calculate_score_remaining_to_close(list('}}>}>))))')))
        self.assertEqual(995444, calculate_score_remaining_to_close(list(']]}}]}]}>')))

    def test_xyz(self):
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
        self.assertEqual(288957, find_middle_score_of_remaining_to_close(lines))

    def test_puzzle_2(self):
        lines = read_lines('input_day10.txt')
        self.assertEqual(3249889609, find_middle_score_of_remaining_to_close(lines))
