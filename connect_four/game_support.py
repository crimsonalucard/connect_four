from functools import reduce
from typing import List, Union, Tuple

from connect_four import GameState, init_game_state
from connect_four.utils import flatten


# checks to see if making a move is valid...
def is_move_valid(game_state: GameState, column: int, row: int) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    return 0 <= column < dimensions_x and 0 <= row < dimensions_y and is_cell_empty(game_state, column, row)


# checks to see if there are pieces other then None, red or yellow.
def are_there_invalid_pieces(game_state: GameState) -> bool:
    def inner(pieces: List[Union[str, None]]) -> bool:
        if len(pieces) == 0:
            return False
        return True if pieces[0] is not None and pieces[0] != 'r' and pieces[0] != 'y' else inner(pieces[1:])

    return inner(flatten(game_state))


# given a column and a row determines whether it is empty
def is_cell_empty(game_state: List[List[str]], column: int, row: int) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    return 0 <= column < dimensions_x and 0 <= row < dimensions_y and game_state[row][column] is None


"""
# the algorithm will try to play a simulated game and attempt to reach the final game state. It will only
# place pieces onto the simulated board if an identical piece already exists in the original game_state.

example:
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

Additionally the algorithm will check to see the game was continued to be played after someone won. This is also 
considered invalid...
So while this game is valid (y did the last move and won)
[r, , , ]
[r, , , ]
[r, , , ]
[y,y,y,y]
This is not, because r moved after the game was won by y:
[r, , , ]
[r, , , ]
[r, , ,r] <--- r's last move
[y,y,y,y]
"""


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

    return _is_state_valid(game_state, init_game_state(dimension_y, dimension_x), 'y', False) and \
        not are_there_invalid_pieces(game_state)


# checks from index if there is a winning diagonal row that goes down and left
def is_n_in_a_diag_row_left(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    if column < 0 or column >= dimensions_x or row < 0 or row >= dimensions_y:
        return False
    elif n == 1:
        return game_state[row][column] == piece
    else:
        return game_state[row][column] == piece and is_n_in_a_diag_row_left(game_state, n - 1, column - 1, row + 1,
                                                                            piece)


# checks from index if there is a winning diagonal row that goes down and right
def is_n_in_a_diag_row_right(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    if column < 0 or column >= dimensions_x or row < 0 or row >= dimensions_y:
        return False
    elif n == 1:
        return game_state[row][column] == piece
    else:
        return game_state[row][column] == piece and is_n_in_a_diag_row_right(game_state, n - 1, column + 1, row + 1,
                                                                             piece)


# checks from index if there is a winning column that goes down
def is_n_in_a_vertical_column(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    if column < 0 or column >= dimensions_x or row < 0 or row >= dimensions_y:
        return False
    elif n == 1:
        return game_state[row][column] == piece
    else:
        return game_state[row][column] == piece and is_n_in_a_vertical_column(game_state, n - 1, column, row + 1, piece)


# checks from index if there is a winning row that goes right
def is_n_in_a_horizontal_row(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    if column < 0 or column >= dimensions_x or row < 0 or row >= dimensions_y:
        return False
    elif n == 1:
        return game_state[row][column] == piece
    else:
        return game_state[row][column] == piece and \
               is_n_in_a_horizontal_row(game_state, n - 1, column + 1, row, piece)


# checks from index if there is a winning right row, down column, or left-down diagonal or right down-diagonal
def is_n_in_a_row(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    return is_n_in_a_horizontal_row(game_state, n, column, row, piece) or \
           is_n_in_a_vertical_column(game_state, n, column, row, piece) or \
           is_n_in_a_diag_row_right(game_state, n, column, row, piece) or \
           is_n_in_a_diag_row_left(game_state, n, column, row, piece)


# checks if the game has a winner
def does_game_have_a_winner(game_state: GameState) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    index_combinations: List[Tuple[int, int]] = [(j, i) for i in range(dimensions_y) for j in range(dimensions_x)]
    did_y_win = reduce(lambda acc, x: acc or is_n_in_a_row(game_state, 4, *x, piece='y'), index_combinations, False)
    did_r_win = reduce(lambda acc, x: acc or is_n_in_a_row(game_state, 4, *x, piece='r'), index_combinations, False)
    return did_y_win or did_r_win


# places a piece into the correct row when given a column
def place_piece(game_state: GameState, piece: str, column: int) -> GameState:
    row: int = find_valid_empty_row(game_state, column)
    return update_game_state(game_state, piece, column, row) if \
        is_state_valid(game_state) and is_move_valid(game_state, column, row) else game_state


# copies game state with a new piece at the specified indexes O(n) runtime due to functional style
def update_game_state(game_state: GameState, piece: str, column: int, row: int) -> GameState:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    return [[piece if j == column and i == row else game_state[i][j] for j in range(dimensions_x)] for i in
            range(dimensions_y)]


# find a row number given an column, that a piece will fall into when placed from the top
def find_valid_empty_row(game_state: GameState, column: int) -> int:
    def inner(game_state_inner: GameState, column_inner: int, row: int) -> int:
        is_current_cell_empty: bool = is_cell_empty(game_state_inner, column_inner, row)
        if row == (len(game_state) - 1) and is_current_cell_empty:
            return row
        elif is_current_cell_empty:
            return inner(game_state_inner, column_inner, row + 1)
        else:
            return row - 1

    empty_row: int = inner(game_state, column, 0)
    return empty_row if 0 <= empty_row < len(game_state) else -1


# counts the amount of the given piece in the game.
def count_pieces(game_state: GameState, piece: str) -> int:
    return reduce(lambda acc, i: acc + 1 if i == piece else acc, flatten(game_state), 0)
