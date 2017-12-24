from functools import reduce
from typing import Union, List, Tuple

from connect_four import GameState, init_game_state
from connect_four.game_support import does_game_have_a_winner, place_piece, count_pieces, find_valid_empty_row, \
    update_game_state, are_there_invalid_pieces
import connect_four.utils


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


# # IO function, untestable (for manual testing)
# # allows you to play a game
# def game_loop(game_state: GameState) -> None:
#     connect_four.utils.clear_screen()
#     show_game_state(game_state)
#     if not is_state_valid(game_state):
#         print("Game state is not valid... exiting...")
#         return None
#     if does_game_have_a_winner(game_state):
#         print("Game is won.")
#         return None
#     player_turn: str = get_player_turn(game_state)
#     print("It is {0}'s turn. ".format(player_turn))
#     column: int = int(input("Enter a column: "))
#     game_loop(auto_play(game_state, column))
#
#
#
# # the algorithm will try to play a simulated game and attempt to reach the final game state. It will only
# # place pieces onto the simulated board if an identical piece already exists in the original game_state.
#
# example:
# Given a 4x4 game_state the following game is impossible if y moves first:
# [r, , , ]
# [r, , , ]
# [y, , , ]
# [y, , , ]
# while the following is valid:
# [ , , , ]
# [ , , , ]
# [ , , , ]
# [y,y,r,r]
#
# The algorithm below will be able to differentiate between such states.
#
# Additionally the algorithm will check to see the game was continued to be played after someone won. This is also
# considered invalid...
# So while this game is valid (y did the last move and won)
# [r, , , ]
# [r, , , ]
# [r, , , ]
# [y,y,y,y]
# This is not, because r moved after the game was won by y:
# [r, , , ]
# [r, , , ]
# [r, , ,r] <--- r's last move
# [y,y,y,y]
def is_state_valid(game_state: GameState) -> bool:
    dimension_x: int = len(game_state[0])
    dimension_y: int = len(game_state)

    def _is_state_valid(game_state_inner: GameState, test_game_state: GameState, piece: str,
                        was_last_game_won: bool) -> bool:
        dimension_x_inner: int = len(game_state_inner[0])
        open_positions: List[Tuple[int, int]] = [(column, find_valid_empty_row(test_game_state, column)) for
                                                 column in
                                                 range(dimension_x_inner)]
        valid_positions: List[Tuple[int, int]] = [i for i in open_positions if
                                                  i[1] >= 0 and game_state_inner[i[1]][i[0]] == piece]

        if len(valid_positions) == 0:  # no more moves left, does the simulated game equal the game_state?
            return game_state_inner == test_game_state
        # game was already won, because there are valid moves still on the board, the game is invalid because
        # a winning game is the last move, there can no additional moves left.
        elif was_last_game_won:
            return False
        else:
            updated_game_states: List[GameState] = [update_game_state(test_game_state, piece, *i) for i in
                                                    valid_positions]
            did_game_wins = [does_game_have_a_winner(i) for i in updated_game_states]
            return reduce(
                lambda acc, x: acc or _is_state_valid(game_state_inner, x[1], 'y' if piece == 'r' else 'r',
                                                      x[0]),
                zip(did_game_wins, updated_game_states), False)

    return not are_there_invalid_pieces(game_state) and _is_state_valid(game_state,
                                                                        init_game_state(dimension_y, dimension_x), 'y',
                                                                        False)
