from typing import List, Union, Tuple
from functools import reduce

from connect_four import GameState
from connect_four.game_state_win_detection import is_n_in_a_row
from connect_four.game_validity_checkers import count_pieces, is_state_valid
from connect_four.move_methods import place_piece, find_valid_empty_row, update_game_state
import connect_four.utils


# initializes an empty game_state with dimensions: size x size
def init_game_state(size_y: int, size_x: int) -> GameState:
    return [[None for _ in range(size_x)] for _ in range(size_y)]


# WARNING: RETURNS NONE. function will bypass type checkers.
# returns the current players turn, given game_state
def get_player_turn(game_state: GameState) -> Union[None, str]:
    amount_of_reds: int = count_pieces(game_state, 'r')
    amount_of_yellows: int = count_pieces(game_state, 'y')
    return ('r' if amount_of_yellows > amount_of_reds else 'y') if is_state_valid(game_state) else None


# automatically play the game based on which players turn. Will not do anything to the gamestate if it is invalid.
def auto_play(game_state: GameState, column: int) -> GameState:
    player_turn: Union[str, None] = get_player_turn(game_state)
    return place_piece(game_state, player_turn, column) if player_turn is not None else game_state


# play function that doesn't do anything if piece parameter does not equal current players' turn.
def play(game_state: GameState, column: int, piece: str) -> GameState:
    return auto_play(game_state, column) if piece == get_player_turn(game_state) else game_state


# determine if there is a winner
def does_game_have_a_winner(game_state: GameState) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    index_combinations: List[Tuple[int, int]] = [(j, i) for i in range(dimensions_y) for j in range(dimensions_x)]
    did_y_win = reduce(lambda acc, x: acc or is_n_in_a_row(game_state, 4, *x, piece='y'), index_combinations, False)
    did_r_win = reduce(lambda acc, x: acc or is_n_in_a_row(game_state, 4, *x, piece='r'), index_combinations, False)
    return (did_y_win or did_r_win) and is_state_valid(game_state)


# IO function, untestable (for manual testing)
# prints what a given game_state looks like.
def show_game_state(game_state: GameState) -> None:
    print(" " + "".join(["_" for _ in range(len(game_state[0]))]))
    for row in game_state:
        acc = ""
        for col in row:
            acc += "_" if col is None else col
        print("|" + acc + "|")
    print(" ")


# IO function, untestable (for manual testing)
# allows you to play a game
def game_loop(game_state: GameState) -> None:
    connect_four.utils.clear_screen()
    show_game_state(game_state)
    if not is_state_valid(game_state):
        print("Game state is not valid... exiting...")
        return None
    if does_game_have_a_winner(game_state):
        print("Game is won.")
        return None
    player_turn: str = get_player_turn(game_state)
    print("It is {0}'s turn. ".format(player_turn))
    column: int = int(input("Enter a column: "))
    game_loop(auto_play(game_state, column))


"""
# brute force algorithm
# the algorithm will try to play a simulated game and attempt to reach the final game state. It will only
# place pieces onto the simulated board if an identical piece already exists in the original game_state.
# For example:
Given a 4x4 game_state the following game is impossible if y moves first:
[r, , , ]
[r, , , ]
[y, , , ]
[y, , , ]
while the following is valid:
[ , , , ]
[ , , , ]
[ , , , ]
[y,y,r,r]

The algorithm below will be able to differentiate between such states. 

This algorithm exists seperate from the gameloop which uses a faster but not nearly as robust game_state. I did this 
because the following function has an upper bound of O(n^m) for an mxn game_state

Additionally the algorithm will check to see the game was continued to be played after someone won. This is also considered
invalid...
So while this game is valid 
[r, , , ]
[r, , , ]
[r, , , ]
[y,y,y,y]
This is not, because r moved after the game was won by y:
[r, , , ]
[r, , , ]
[r, , ,r]
[y,y,y,y]
"""


def is_state_configuration_valid(game_state: GameState) -> bool:
    dimension_x: int = len(game_state[0])
    dimension_y: int = len(game_state)

    def _is_state_configuration_valid(game_state: GameState, test_game_state: GameState, piece: str,
                                      was_last_game_won: bool) -> bool:
        dimension_x_inner: int = len(game_state[0])
        valid_positions: List[Tuple[int, int]] = [(column, find_valid_empty_row(test_game_state, column)) for
                                                  column in
                                                  range(dimension_x_inner)]
        valid_positions: List[Tuple[int, int]] = [i for i in valid_positions if
                                                  i[1] >= 0 and game_state[i[1]][i[0]] == piece]
        if len(valid_positions) == 0:  # no more moves left, does the simulated game equal the game_state?
            return game_state == test_game_state
        # game was already won, because there are valid moves still on the board, the game is invalid because
        # a winning game is the last move, there can no additional moves left.
        elif was_last_game_won:
            return False
        else:
            updated_game_states: List[GameState] = [update_game_state(test_game_state, piece, *i) for i in
                                                    valid_positions]
            did_game_wins = [does_game_have_a_winner(i) for i in updated_game_states]
            return reduce(
                lambda acc, x: acc or _is_state_configuration_valid(game_state, x[1], 'y' if piece == 'r' else 'r',
                                                                    x[0]),
                zip(did_game_wins, updated_game_states), False)

    return _is_state_configuration_valid(game_state, init_game_state(dimension_y, dimension_x), 'y', False)
