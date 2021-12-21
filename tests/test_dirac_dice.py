import unittest


class Player:
    def __init__(self, position):
        self.position = position
        self.score = 0


def evolve(players):
    dice_face = 1
    player_index = 0
    iterations = 0
    while all(p.score < 1000 for p in players):
        player = players[player_index]
        dice_rolls_sum = 3 * dice_face + 3
        player.position = next_position(player, dice_rolls_sum)
        player.score += player.position
        iterations += 1
        dice_face = dice_face + 3
        player_index = (player_index + 1) % 2
    return iterations * 3


def next_position(player, score):
    new_position = (player.position - 1) + score
    return (new_position % 10) + 1


class DiracDiceTest(unittest.TestCase):
    def test_evolve(self):
        p1 = Player(4)
        p2 = Player(8)
        number_of_rolls = evolve([p1, p2])
        self.assertEqual(739785, min(p1.score, p2.score) * number_of_rolls)

    def test_puzzle_1(self):
        p1 = Player(2)
        p2 = Player(1)
        number_of_rolls = evolve([p1, p2])
        self.assertEqual(797160, min(p1.score, p2.score) * number_of_rolls)
