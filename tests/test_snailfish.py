import unittest
from math import floor, ceil

from advent_of_code.utilities import read_lines


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __repr__(self):
        return f"[{self.left},{self.right}]"

    def __add__(self, other):
        return Pair(self, other)

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()


class Value:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"{self.value}"

    def magnitude(self):
        return self.value


def split_number(number):
    if type(number.left) == Value and number.left.value >= 10:
        regular_number = number.left.value
        number.left = Pair(Value(floor(regular_number / 2)), Value(ceil(regular_number / 2)))
        return True
    if type(number.left) == Pair and split_number(number.left):
        return True
    if type(number.right) == Value and number.right.value >= 10:
        regular_number = number.right.value
        number.right = Pair(Value(floor(regular_number / 2)), Value(ceil(regular_number / 2)))
        return True
    if type(number.right) == Pair and split_number(number.right):
        return True
    return False


def next_explosion(pair, current_path):
    if type(pair) == Value:
        return None
    if len(current_path) == 4:
        return current_path, pair
    candidate = next_explosion(pair.left, current_path + ['left'])
    if candidate is not None:
        return candidate
    return next_explosion(pair.right, current_path + ['right'])


def explode(pair, path, root):
    handle_left(pair, path, root)
    handle_right(pair, path, root)
    ## change value
    value_to_add = root
    for t in path[:-1]:
        if t == 'left':
            value_to_add = value_to_add.left
        else:
            value_to_add = value_to_add.right
    if path[-1] == 'left':
        value_to_add.left = Value(0)
    else:
        value_to_add.right = Value(0)


def handle_right(pair, path, root):
    sub_path = last_turn(path, 'left')
    if sub_path is None:
        return
    last = sub_path[:-1] + ['right']
    value_to_add = root
    for t in last:
        if t == 'left':
            value_to_add = value_to_add.left
        else:
            value_to_add = value_to_add.right
    while type(value_to_add) != Value:
        value_to_add = value_to_add.left
    value_to_add.value += pair.right.value


def handle_left(pair, path, root):
    sub_path = last_turn(path, 'right')
    if sub_path is None:
        return
    last = sub_path[:-1] + ['left']
    value_to_add = root
    for t in last:
        if t == 'left':
            value_to_add = value_to_add.left
        else:
            value_to_add = value_to_add.right
    while type(value_to_add) != Value:
        value_to_add = value_to_add.right
    value_to_add.value += pair.left.value

def last_turn(path, position):
    try:
        index = len(path) - 1 - path[::-1].index(position)
        return path[:index + 1]
    except:
        return None

def reduce_number(root):
    while True:
        while True:
            explosion = next_explosion(root, [])
            if explosion is None:
                break
            path, pair = explosion
            explode(pair, path, root)
        if not split_number(root):
            return


def parse_raw_pair(raw_expression):
    return parse_pair(eval(raw_expression))


def parse_pair(expression):
    if type(expression) == int:
        return Value(expression)
    left, right = expression
    return Pair(
        parse_pair(left),
        parse_pair(right)
    )


def add_raw_numbers(raw_numbers):
    number = parse_raw_pair(raw_numbers[0])
    reduce_number(number)
    for raw_number in raw_numbers[1:]:
        addend = parse_raw_pair(raw_number)
        number = number + addend
        reduce_number(number)
    return number


class Snailfish(unittest.TestCase):
    def test_parse_expression(self):
        self.assertEqual('[[1,2],3]', str(parse_raw_pair('[[1,2],3]')))
        raw_pair = '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]'
        self.assertEqual(raw_pair, str(parse_raw_pair(raw_pair)))

    def test_addition(self):
        left = parse_raw_pair('[[[[4,3],4],4],[7,[[8,4],9]]]')
        right = parse_raw_pair('[1,1]')
        expected = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
        self.assertEqual(expected, str(left + right))

    def test_explode(self):
        self.assertExplosion('[[[[0,9],2],3],4]', '[[[[[9,8],1],2],3],4]')
        self.assertExplosion('[7,[6,[5,[7,0]]]]', '[7,[6,[5,[4,[3,2]]]]]')
        self.assertExplosion('[[6,[5,[7,0]]],3]', '[[6,[5,[4,[3,2]]]],1]')
        self.assertExplosion('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')
        self.assertExplosion('[[3,[2,[8,0]]],[9,[5,[7,0]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')

    def test_find_candidate_explosion(self):
        root = parse_raw_pair('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
        path, pair = next_explosion(root, [])
        self.assertEqual(['left', 'left', 'left', 'left'], path)
        self.assertEqual('[4,3]', str(pair))
        explode(pair, path, root)
        self.assertEqual('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]', str(root))

        path, pair = next_explosion(root, [])
        self.assertEqual(['left', 'right', 'right', 'left'], path)
        self.assertEqual('[8,4]', str(pair))
        explode(pair, path, root)
        self.assertEqual('[[[[0,7],4],[15,[0,13]]],[1,1]]', str(root))

    def test_reduce_number(self):
        root = parse_raw_pair('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')
        reduce_number(root)
        self.assertEqual('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', str(root))

    def test_sum_number(self):
        raw_numbers = ['[1, 1]',
                       '[2, 2]',
                       '[3, 3]',
                       '[4, 4]']
        number = add_raw_numbers(raw_numbers)
        self.assertEqual('[[[[1,1],[2,2]],[3,3]],[4,4]]', str(number))

        raw_numbers = ['[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]',
                       '[7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]',
                       '[[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]]',
                       '[[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]]',
                       '[7, [5, [[3, 8], [1, 4]]]]',
                       '[[2, [2, 2]], [8, [8, 1]]]',
                       '[2, 9]',
                       '[1, [[[9, 3], 9], [[9, 0], [0, 7]]]]',
                       '[[[5, [7, 4]], 7], 1]',
                       '[[[[4, 2], 2], 6], [8, 7]]']
        number = add_raw_numbers(raw_numbers)
        self.assertEqual('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', str(number))
        self.assertEqual(3488, number.magnitude())

    def assertExplosion(self, exploded, original):
        root = parse_raw_pair(original)
        path, pair = next_explosion(root, [])
        explode(pair, path, root)
        self.assertEqual(exploded, str(root))
