import unittest
from collections import defaultdict
from itertools import product


class Player:
    def __init__(self, position, score=0):
        self.position = position
        self.score = score

    def roll_dirac(self, n):
        self.position = (self.position + n - 1) % 10 + 1
        self.score = self.score + self.position


# from itertools import combinations_with_replacement
# list(combinations_with_replacement([1,2,3], 3))

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


def dirac_combinations():
    combinations = product([1, 2, 3], repeat=3)
    dice_roll_sums = defaultdict(lambda: 0)
    for c in combinations:
        dice_roll_sums[sum(c)] += 1
    return dice_roll_sums


def dirac_game(position_player1, score_player1, position_player2, score_player2, turn, dice_roll_sum, memo):
    if (position_player1, score_player1, position_player2, score_player2, turn) in memo:
        return memo[(position_player1, score_player1, position_player2, score_player2, turn)]
    if score_player1 >= 21:
        memo[(position_player1, score_player1, position_player2, score_player2, turn)] = [1, 0]
        return [1, 0]
    if score_player2 >= 21:
        memo[(position_player1, score_player1, position_player2, score_player2, turn)] = [0, 1]
        return [0, 1]
    victories = [0, 0]
    for roll_sum, number_of_occurrences in dice_roll_sum.items():
        if turn == 'player1':
            player1 = Player(position_player1, score_player1)
            player1.roll_dirac(roll_sum)
            roll_sum_victories = dirac_game(player1.position, player1.score, position_player2, score_player2, 'player2',
                                            dice_roll_sum, memo)
        else:
            player2 = Player(position_player2, score_player2)
            player2.roll_dirac(roll_sum)
            roll_sum_victories = dirac_game(position_player1, score_player1, player2.position, player2.score, 'player1',
                                            dice_roll_sum, memo)
        victories[0] += roll_sum_victories[0] * number_of_occurrences
        victories[1] += roll_sum_victories[1] * number_of_occurrences
    memo[(position_player1, score_player1, position_player2, score_player2, turn)] = victories
    return victories


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

    def test_dirac_game_simple(self):
        space_player1 = 4
        space_player2 = 8
        score_player1, score_player2 = 0, 0
        dice_roll_sums = dirac_combinations()
        victories = dirac_game(space_player1, score_player1, space_player2, score_player2, 'player1', dice_roll_sums,
                               {})
        self.assertEqual([444356092776315, 341960390180808], victories)

    def test_puzzle2(self):
        space_player1 = 2
        space_player2 = 1
        score_player1, score_player2 = 0, 0
        dice_roll_sums = dirac_combinations()
        victories = dirac_game(space_player1, score_player1, space_player2, score_player2, 'player1', dice_roll_sums,
                               {})
        self.assertEqual([27464148626406, 22909380722959], victories)
        self.assertEqual(27464148626406, max(victories))
