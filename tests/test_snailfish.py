import unittest
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


class Value:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"{self.value}"


def reduce_number(root):
    while True:
        explosion = next_explosion(root, [])
        if explosion is None:
            break
        path, pair = explosion
        explode(pair, path, root)


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
        self.assertEqual('[[[[0,7],4],[15,[0,13]]],[1,1]]', str(root))

    def assertExplosion(self, exploded, original):
        root = parse_raw_pair(original)
        path, pair = next_explosion(root, [])
        explode(pair, path, root)
        self.assertEqual(exploded, str(root))

# right left -> add to last element of left, right
# left left ->

# find last right and instead of going ok the right go to the last value on left -> right

def last_turn(path, position):
    try:
        index = len(path) - 1 - path[::-1].index(position)
        print(index)
        return path[:index + 1]
    except:
        return None
