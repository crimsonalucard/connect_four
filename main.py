from typing import List, Any, Union
from functools import reduce

# type aliases
GameState = List[List[Union[None, str]]]


def init_game_state(size: int) -> GameState:
    return [[None for _ in range(size)] for _ in range(size)]


def flatten(list_of_lists: List[List[Any]]):
    return [item for sublist in list_of_lists for item in sublist]


def count_pieces(game_state: GameState, piece: str) -> int:
    return reduce(lambda acc, i: acc + 1 if i == piece else acc, flatten(game_state), 0)


def is_move_valid(game_state: GameState, column: int, row: int) -> bool:
    dimensions: int = len(game_state)
    return is_cell_empty(game_state, column, row) and 0 <= column < dimensions and 0 <= row < dimensions


def are_amount_of_pieces_valid(game_state: GameState) -> bool:
    amount_of_reds: int = count_pieces(game_state, 'r')
    amount_of_yellows: int = count_pieces(game_state, 'y')
    return amount_of_reds == amount_of_yellows or amount_of_reds == amount_of_yellows - 1


def are_there_pieces_with_empty_spots_below(game_state: GameState) -> bool:
    def does_piece_have_empty_space_below(game_state_inner: GameState, column_inner: int, row_inner: int) -> bool:
        dimensions_inner: int = len(GameState)
        return 0 <= column_inner < dimensions_inner and 0 <= row_inner < dimensions_inner - 1 and \
            game_state_inner[row_inner + 1][column_inner] is None

    dimensions: int = len(game_state)
    index_combinations: List[List[int]] = ((i, j) for i in range(dimensions) for j in range(dimensions))
    return reduce(lambda acc, x: acc and does_piece_have_empty_space_below(game_state, *x), index_combinations, True)


def is_game_valid(game_state: GameState) -> bool:
    return are_amount_of_pieces_valid(game_state) and are_there_pieces_with_empty_spots_below(game_state)


# create new game state with results updated. O(n^2) due to immuteability of gamestate.
def update_game_state(game_state: GameState, piece: str, column: int, row: int) -> GameState:
    dimensions: int = len(game_state)
    return [[piece if j == column and i == row else game_state[i][j] for j in range(dimensions)] for i in
            range(dimensions)]


# place a piece from the top and return the new gamestate
def place_piece(game_state: GameState, piece: str, column: int) -> GameState:
    row: int = find_valid_empty_row(game_state, column)
    return update_game_state(game_state, piece, column, row) if \
        is_game_valid(game_state) and is_move_valid(game_state, column, row) else game_state


# given a column and a row determines whether it is empty
def is_cell_empty(game_state: List[List[str]], column: int, row: int) -> bool:
    return game_state[row][column] is None


# given a column and gamestate finds the row index where the next piece should be placed.
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


def get_player_turn(game_state: GameState) -> str:
    amount_of_reds: int = count_pieces(game_state, 'r')
    amount_of_yellows: int = count_pieces(game_state, 'y')
    return ('r' if amount_of_yellows > amount_of_reds else 'y') if is_game_valid(game_state) else game_state
