from typing import List, Union
from functools import reduce

from connect_four import GameState
from connect_four.game_state_win_detection import is_n_in_a_row
from connect_four.game_validity_checkers import count_pieces, is_game_valid
from connect_four.move_methods import place_piece
import connect_four.utils


# initializes an empty game_state with dimensions: size x size
def init_game_state(size_y: int, size_x: int) -> GameState:
    return [[None for _ in range(size_x)] for _ in range(size_y)]


# WARNING: RETURNS NONE. function will bypass type checkers.
# returns the current players turn, given game_state
def get_player_turn(game_state: GameState) -> Union[None, str]:
    amount_of_reds: int = count_pieces(game_state, 'r')
    amount_of_yellows: int = count_pieces(game_state, 'y')
    return ('r' if amount_of_yellows > amount_of_reds else 'y') if is_game_valid(game_state) else None


# automatically play the game based on which players turn. Will not do anything to the gamestate if it is invalid.
def auto_play(game_state: GameState, column: int) -> GameState:
    player_turn: Union[str, None] = get_player_turn(game_state)
    return place_piece(game_state, player_turn, column) if player_turn is not None else game_state


# play function that doesn't do anything if piece parameter does not equal current players' turn.
def play(game_state: GameState, column: int, piece: str) -> GameState:
    return auto_play(game_state, column) if piece == get_player_turn(game_state) else game_state


# determine if there is a winner
def does_game_have_a_winner(game_state: GameState) -> bool:
    dimensions_x: int = len(game_state)
    dimensions_y: int = len(game_state[0])
    index_combinations: List[List[int]] = [(j, i) for i in range(dimensions_x) for j in range(dimensions_y)]
    did_y_win = reduce(lambda acc, x: acc or is_n_in_a_row(game_state, 4, *x, piece='y'), index_combinations, False)
    did_r_win = reduce(lambda acc, x: acc or is_n_in_a_row(game_state, 4, *x, piece='r'), index_combinations, False)
    return (did_y_win or did_r_win) and is_game_valid(game_state)


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
def game_loop(game_state) -> None:
    connect_four.utils.clear_screen()
    show_game_state(game_state)
    if not is_game_valid(game_state):
        print("Game state is not valid... exiting...")
        return
    if does_game_have_a_winner(game_state):
        print("Game is won.")
        return
    player_turn: str = get_player_turn(game_state)
    print("It is {0}'s turn. ".format(player_turn))
    column: int = int(input("Enter a column: "))
    game_loop(auto_play(game_state, column))
