from unittest import TestCase
from connect_four.game import \
    get_player_turn, \
    auto_play, \
    play, \
    show_game_state
from connect_four import init_game_state
from connect_four.utils import flatten
from connect_four.game_support import \
    is_move_valid, are_there_invalid_pieces, \
    is_cell_empty, \
    is_state_valid, is_state_valid, is_n_in_a_diag_row_left, is_n_in_a_diag_row_right, \
    is_n_in_a_vertical_column, is_n_in_a_horizontal_row, is_n_in_a_row, does_game_have_a_winner, place_piece, \
    update_game_state, find_valid_empty_row, count_pieces
from connect_four.obsolete_functions import are_there_pieces_with_empty_spots_below, are_amount_of_pieces_valid


class TestMain(TestCase):
    def setUp(self):
        self.game_state1 = [[None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, "r", None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, "y", None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, "y", None, "r", None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, "r", None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None]]
        self.game_state2 = [[None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, 'y', 'r', 'y']]
        self.game_state3 = [[None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, 'r', 'y']]
        self.game_state4 = [[None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, 'r', None],
                            [None, None, None, None, None, None, None, None, 'r', 'y']]
        self.game_state5 = [[None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, 'x', None],
                            [None, None, None, None, None, None, None, None, 'r', 'y']]
        self.game_state6 = [[None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, 'y', None],
                            [None, None, None, None, None, None, None, None, 'r', 'y']]
        self.game_state = [[None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None],
                           [None, None, None, None, None, None, None, None, None, None]]
        self.game_state7 = [[None, None, None, None, None, None, None, None, None, "r"],
                            [None, None, None, None, None, None, None, None, None, "y"],
                            [None, None, None, None, None, None, None, None, None, "r"],
                            [None, None, None, None, None, None, None, None, None, "y"],
                            [None, None, None, None, None, None, None, None, None, "r"],
                            [None, None, None, None, None, None, None, None, None, "y"],
                            [None, None, None, None, None, None, None, None, None, "r"],
                            [None, None, None, None, None, None, None, None, None, "y"],
                            [None, None, None, None, None, None, None, None, None, "r"],
                            [None, None, None, None, None, None, None, None, None, "y"]]
        self.game_state1a = [[None, None, None, None, None, None, "r"],
                             [None, None, "y", None, "r", None, None],
                             [None, None, None, None, None, "y", None],
                             [None, None, None, "r", None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None]]
        self.game_state2a = [[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, 'y', 'r', 'y']]
        self.game_state3a = [[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, 'r', 'y']]
        self.game_state4a = [[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, 'r', None],
                             [None, None, None, None, None, 'r', 'y']]
        self.game_state5a = [[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, 'x', None],
                             [None, None, None, None, None, 'r', 'y']]
        self.game_state6a = [[None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, None, None],
                             [None, None, None, None, None, 'y', None],
                             [None, None, None, None, None, 'r', 'y']]
        self.game_statea = [[None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None]]
        self.game_state7a = [[None, None, None, None, None, None, "r"],
                             [None, None, None, None, None, None, "y"],
                             [None, None, None, None, None, None, "r"],
                             [None, None, None, None, None, None, "y"],
                             [None, None, None, None, None, None, "r"],
                             [None, None, None, None, None, None, "y"]]
        self.game_state8a = [[None, None, None, None, None, None, "r"],
                             [None, None, None, None, None, None, "y"],
                             [None, None, None, "y", None, None, "r"],
                             [None, None, None, "r", "y", None, "y"],
                             [None, None, None, "y", "r", "y", "r"],
                             [None, None, None, "r", "r", "y", "y"]]
        self.game_state9a = [[None, None, None, None, None, None, "r"],
                             [None, None, None, None, None, None, "y"],
                             [None, None, None, None, None, None, "r"],
                             [None, None, None, "r", "y", "r", "y"],
                             [None, None, None, "y", "r", "y", "r"],
                             ["y", None, None, "r", "r", "y", "y"]]
        self.invalid_game = [['r', None, None, None],
                             ['r', None, None, None],
                             ['y', None, None, None],
                             ['y', None, None, None]]
        self.valid_game = [[None, None, None, None],
                           [None, None, None, None],
                           [None, None, None, None],
                           ['y', 'y', 'r', 'r']]
        self.valid_game1 = [['r', None, None, None],
                           ['r', None, None, None],
                           ['r', None, None, None],
                           ['y', 'y', 'y', 'y']]
        self.invalid_game1 = [['r', None, None, None],
                             ['r', None, None, None],
                             ['r', None, None, 'r'],
                             ['y', 'y', 'y', 'y']]
        self.invalid_game2 = [[None, None, None, None],
                              [None, None, None, None],
                              ['y', None, None, None],
                              ['r', None, None, None]]
        self.valid_game2 = [['r', None, None, None],
                              ['r', None, None, None],
                              ['r', None, None, 'y'],
                              ['y', 'y', 'y', 'r']]

    def test_init_game_state(self):
        self.assertEqual(init_game_state(10, 10), self.game_state)
        self.assertEqual(init_game_state(6, 7), self.game_statea)

    def test_flattern(self):
        x = [[1], [2, 3], [4, 5, 6]]
        self.assertEqual(flatten(x), [1, 2, 3, 4, 5, 6])

    def test_count_pieces(self):
        self.assertEqual(count_pieces(self.game_state1, 'x'), 0)
        self.assertEqual(count_pieces(self.game_state1, 'r'), 3)
        self.assertEqual(count_pieces(self.game_state1, 'y'), 2)
        self.assertEqual(count_pieces(self.game_state1a, 'x'), 0)
        self.assertEqual(count_pieces(self.game_state1a, 'r'), 3)
        self.assertEqual(count_pieces(self.game_state1a, 'y'), 2)

    def test_is_cell_empty(self):
        self.assertTrue(is_cell_empty(self.game_state1, 0, 0))
        self.assertFalse(is_cell_empty(self.game_state1, 3, 3))
        self.assertTrue(is_cell_empty(self.game_state1a, 0, 0))
        self.assertFalse(is_cell_empty(self.game_state1a, 3, 3))

    def test_is_move_valid(self):
        self.assertFalse(is_move_valid(self.game_state1, 20, 30))
        self.assertFalse(is_move_valid(self.game_state1, -20, -30))
        self.assertFalse(is_move_valid(self.game_state1, 3, 3))
        self.assertTrue(is_move_valid(self.game_state1, 3, 4))
        self.assertFalse(is_move_valid(self.game_state1a, 20, 30))
        self.assertFalse(is_move_valid(self.game_state1a, -20, -30))
        self.assertFalse(is_move_valid(self.game_state1a, 3, 3))
        self.assertTrue(is_move_valid(self.game_state1a, 3, 4))

    def test_are_amount_of_pieces_valid(self):
        self.assertTrue(are_amount_of_pieces_valid(self.game_state2))
        self.assertTrue(are_amount_of_pieces_valid(self.game_state3))
        self.assertFalse(are_amount_of_pieces_valid(self.game_state4))
        self.assertTrue(are_amount_of_pieces_valid(self.game_state2a))
        self.assertTrue(are_amount_of_pieces_valid(self.game_state3a))
        self.assertFalse(are_amount_of_pieces_valid(self.game_state4a))

    def test_are_there_pieces_with_empty_spots_below(self):
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state))
        self.assertTrue(are_there_pieces_with_empty_spots_below(self.game_state1))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state2))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state3))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state4))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_statea))
        self.assertTrue(are_there_pieces_with_empty_spots_below(self.game_state1a))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state2a))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state3a))
        self.assertFalse(are_there_pieces_with_empty_spots_below(self.game_state4a))

    def test_are_there_invalid_pieces(self):
        self.assertFalse(are_there_invalid_pieces(self.game_state))
        self.assertFalse(are_there_invalid_pieces(self.game_state1))
        self.assertFalse(are_there_invalid_pieces(self.game_state2))
        self.assertFalse(are_there_invalid_pieces(self.game_state3))
        self.assertFalse(are_there_invalid_pieces(self.game_state4))
        self.assertTrue(are_there_invalid_pieces(self.game_state5))
        self.assertFalse(are_there_invalid_pieces(self.game_statea))
        self.assertFalse(are_there_invalid_pieces(self.game_state1a))
        self.assertFalse(are_there_invalid_pieces(self.game_state2a))
        self.assertFalse(are_there_invalid_pieces(self.game_state3a))
        self.assertFalse(are_there_invalid_pieces(self.game_state4a))
        self.assertTrue(are_there_invalid_pieces(self.game_state5a))

    def test_is_game_valid(self):
        self.assertTrue(is_state_valid(self.game_state))
        self.assertFalse(is_state_valid(self.game_state1))
        self.assertTrue(is_state_valid(self.game_state2))
        self.assertTrue(is_state_valid(self.game_state3))
        self.assertFalse(is_state_valid(self.game_state4))
        self.assertFalse(is_state_valid(self.game_state5))
        self.assertTrue(is_state_valid(self.game_statea))
        self.assertFalse(is_state_valid(self.game_state1a))
        self.assertTrue(is_state_valid(self.game_state2a))
        self.assertTrue(is_state_valid(self.game_state3a))
        self.assertFalse(is_state_valid(self.game_state4a))
        self.assertFalse(is_state_valid(self.game_state5a))

    def test_get_player_turn(self):
        self.assertEqual(get_player_turn(self.game_state), 'y')
        self.assertIsNone(get_player_turn(self.game_state1))
        self.assertEqual(get_player_turn(self.game_state2), 'r')
        self.assertEqual(get_player_turn(self.game_state3), 'y')
        self.assertIsNone(get_player_turn(self.game_state4))
        self.assertIsNone(get_player_turn(self.game_state5))
        self.assertEqual(get_player_turn(self.game_statea), 'y')
        self.assertIsNone(get_player_turn(self.game_state1a))
        self.assertEqual(get_player_turn(self.game_state2a), 'r')
        self.assertEqual(get_player_turn(self.game_state3a), 'y')
        self.assertIsNone(get_player_turn(self.game_state4a))
        self.assertIsNone(get_player_turn(self.game_state5a))

    def test_find_valid_empty_row(self):
        self.assertEqual(find_valid_empty_row(self.game_state, 0), 9)
        self.assertEqual(find_valid_empty_row(self.game_state, 4), 9)
        self.assertEqual(find_valid_empty_row(self.game_state2, 8), 8)
        self.assertEqual(find_valid_empty_row(self.game_state4, 8), 7)
        self.assertEqual(find_valid_empty_row(self.game_statea, 0), 5)
        self.assertEqual(find_valid_empty_row(self.game_statea, 4), 5)
        self.assertEqual(find_valid_empty_row(self.game_state2a, 6), 4)
        self.assertEqual(find_valid_empty_row(self.game_state4a, 5), 3)

    def test_update_game_state(self):
        x = init_game_state(10, 10)
        x = update_game_state(x, 'y', 9, 9)
        x = update_game_state(x, 'r', 8, 9)
        x = update_game_state(x, 'y', 7, 9)
        self.assertEqual(x, self.game_state2)
        x = init_game_state(6, 7)
        x = update_game_state(x, 'y', 6, 5)
        x = update_game_state(x, 'r', 5, 5)
        x = update_game_state(x, 'y', 4, 5)
        self.assertEqual(x, self.game_state2a)

    def test_place_piece(self):
        x = place_piece(self.game_state, 'y', 9)
        x = place_piece(x, 'r', 8)
        x = place_piece(x, 'y', 7)
        self.assertEqual(x, self.game_state2)
        y = place_piece(self.game_state1, 'y', 2)
        self.assertEqual(y, self.game_state1)

        x = place_piece(self.game_statea, 'y', 6)
        x = place_piece(x, 'r', 5)
        x = place_piece(x, 'y', 4)
        self.assertEqual(x, self.game_state2a)
        y = place_piece(self.game_state1a, 'y', 2)
        self.assertEqual(y, self.game_state1a)

    def test_auto_play(self):
        x = init_game_state(10, 10)
        x = auto_play(x, 9)
        x = auto_play(x, 8)
        x = auto_play(x, 8)
        self.assertEqual(x, self.game_state6)
        y = init_game_state(10, 10)
        for _ in range(30):
            y = auto_play(y, 9)
        self.assertEqual(y, self.game_state7)
        w = auto_play(self.game_state1, 2)
        self.assertEqual(w, self.game_state1)

        x = init_game_state(6, 7)
        x = auto_play(x, 6)
        x = auto_play(x, 5)
        x = auto_play(x, 5)
        self.assertEqual(x, self.game_state6a)
        y = init_game_state(6, 7)
        for _ in range(30):
            y = auto_play(y, 6)

        self.assertEqual(y, self.game_state7a)
        w = auto_play(self.game_state1a, 2)
        self.assertEqual(w, self.game_state1a)

    def test_play(self):
        x = init_game_state(6, 7)
        x = play(x, 6, 'y')
        x = play(x, 5, 'r')
        x = play(x, 5, 'y')
        self.assertEqual(x, self.game_state6a)
        x = init_game_state(6, 7)
        x = play(x, 6, 'r')
        x = play(x, 5, 'r')
        x = play(x, 5, 'r')
        self.assertEqual(x, init_game_state(6, 7))

    def test_is_n_in_a_horizontal_row(self):
        x = init_game_state(6, 7)
        for i in range(4):
            x = auto_play(x, i)
            x = auto_play(x, 0)
        self.assertTrue(is_n_in_a_horizontal_row(x, 4, 0, 5, 'y'))
        x[5][0] = 'r'
        self.assertFalse(is_n_in_a_horizontal_row(x, 4, 0, 5, 'y'))

    def test_is_n_in_a_vertical_row(self):
        x = init_game_state(6, 7)
        for i in range(4):
            x = auto_play(x, i)
            x = auto_play(x, 0)
        self.assertTrue(is_n_in_a_vertical_column(x, 4, 0, 1, 'r'))
        x[4][0] = 'y'
        self.assertFalse(is_n_in_a_vertical_column(x, 4, 0, 1, 'r'))

    def test_is_n_in_a_diag_row_right(self):
        self.assertTrue(is_n_in_a_diag_row_right(self.game_state8a, 4, 3, 2, 'y'))
        self.game_state8a[5][6] = 'r'
        self.assertFalse(is_n_in_a_diag_row_right(self.game_state8a, 4, 3, 2, 'y'))
        self.game_state8a[5][6] = 'y'

    def test_is_n_in_a_diag_row_left(self):
        self.assertFalse(is_n_in_a_diag_row_left(self.game_state8a, 4, 3, 2, 'y'))
        self.game_state8a[5][6] = 'r'
        self.assertFalse(is_n_in_a_diag_row_left(self.game_state8a, 4, 3, 2, 'y'))
        self.game_state8a[5][6] = 'y'
        self.assertTrue(is_n_in_a_diag_row_left(self.game_state9a, 4, 6, 2, 'r'))

    def test_is_n_in_a_row(self):
        x = init_game_state(6, 7)
        for i in range(4):
            x = auto_play(x, i)
            x = auto_play(x, 0)
        self.assertTrue(is_n_in_a_row(x, 4, 0, 5, 'y'))
        x[5][0] = 'r'
        self.assertFalse(is_n_in_a_row(x, 4, 0, 5, 'y'))

        x = init_game_state(6, 7)
        for i in range(4):
            x = auto_play(x, i)
            x = auto_play(x, 0)
        self.assertTrue(is_n_in_a_row(x, 4, 0, 1, 'r'))
        x[4][0] = 'y'
        self.assertFalse(is_n_in_a_row(x, 4, 0, 1, 'r'))

        self.assertTrue(is_n_in_a_row(self.game_state8a, 4, 3, 2, 'y'))
        self.game_state8a[5][6] = 'r'
        self.assertFalse(is_n_in_a_row(self.game_state8a, 4, 3, 2, 'y'))
        self.game_state8a[5][6] = 'y'

        self.assertTrue(is_n_in_a_row(self.game_state9a, 4, 6, 2, 'r'))

    def test_does_game_have_a_winner(self):
        x = init_game_state(6, 7)
        for i in range(4):
            x = auto_play(x, i)
            x = auto_play(x, 0)
        self.assertTrue(does_game_have_a_winner(x))
        x[5][0] = 'r'
        x[4][0] = 'y'
        self.assertFalse(does_game_have_a_winner(x))

        x = init_game_state(6, 7)
        for i in range(4):
            x = auto_play(x, i)
            x = auto_play(x, 0)
        self.assertTrue(does_game_have_a_winner(x))
        x[4][0] = 'y'
        x[5][3] = 'r'
        self.assertFalse(does_game_have_a_winner(x))  # invalid game_state
        x[5][5] = 'r'
        x[4][0] = 'r'
        self.assertTrue(does_game_have_a_winner(x))

        self.assertTrue(does_game_have_a_winner(self.game_state8a))
        self.game_state8a[5][6] = 'r'
        self.assertFalse(does_game_have_a_winner(self.game_state8a))
        self.game_state8a[5][6] = 'y'

        self.assertTrue(does_game_have_a_winner(self.game_state9a))

    def test_is_state_configuration_valid(self):
        self.assertFalse(is_state_valid(self.invalid_game))
        self.assertTrue(is_state_valid(self.valid_game))
        self.assertTrue(is_state_valid(self.valid_game1))
        self.assertFalse(is_state_valid(self.invalid_game1))
        self.assertFalse(is_state_valid(self.invalid_game2))
        self.assertTrue(is_state_valid(self.valid_game2))
        self.assertFalse(is_state_valid(self.game_state1))
        self.assertTrue(is_state_valid(self.game_state2))
        self.assertTrue(is_state_valid(self.game_state3))
        self.assertFalse(is_state_valid(self.game_state4))
        self.assertFalse(is_state_valid(self.game_state5))
        self.assertTrue(is_state_valid(self.game_state6))
        self.assertTrue(is_state_valid(self.game_state))
        self.assertTrue(is_state_valid(self.game_state7))
        self.assertFalse(is_state_valid(self.game_state1a))
        self.assertTrue(is_state_valid(self.game_state2a))
        self.assertTrue(is_state_valid(self.game_state3a))
        self.assertFalse(is_state_valid(self.game_state4a))
        self.assertFalse(is_state_valid(self.game_state5a))
        self.assertTrue(is_state_valid(self.game_state6a))
        self.assertTrue(is_state_valid(self.game_statea))
        self.assertTrue(is_state_valid(self.game_state7a))
        self.assertTrue(is_state_valid(self.game_state8a))
        self.assertTrue(is_state_valid(self.game_state9a))


