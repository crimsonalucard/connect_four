from functools import reduce
from typing import List, Union, Tuple

from connect_four import GameState
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
    return update_game_state(game_state, piece, column, row) if is_move_valid(game_state, column, row) else game_state


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
