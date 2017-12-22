from functools import reduce
from typing import List, Union, Tuple

from connect_four import GameState
from connect_four.utils import flatten


# checks for pieces with empty spaces below
def are_there_pieces_with_empty_spots_below(game_state: GameState) -> bool:
    def does_piece_have_empty_space_below(game_state_inner: GameState, column_inner: int, row_inner: int) -> bool:
        dimensions_inner_y: int = len(game_state_inner)
        dimensions_inner_x: int = len(game_state_inner[0])
        return \
            0 <= column_inner < dimensions_inner_x and \
            0 <= row_inner < dimensions_inner_y - 1 and \
            game_state_inner[row_inner + 1][column_inner] is None and \
            game_state_inner[row_inner][column_inner] is not None

    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    index_combinations: List[Tuple[int, int]] = [(i, j) for i in range(dimensions_x) for j in range(dimensions_y)]
    return reduce(lambda acc, x: acc or does_piece_have_empty_space_below(game_state, *x), index_combinations, False)


# checks to see if reds relative to yellows are correct in numbers satisfying the proposition: y == r or r + 1 == y
def are_amount_of_pieces_valid(game_state: GameState) -> bool:
    amount_of_reds: int = count_pieces(game_state, 'r')
    amount_of_yellows: int = count_pieces(game_state, 'y')
    return amount_of_reds == amount_of_yellows or amount_of_reds == amount_of_yellows - 1


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


# counts the selected piece.
def count_pieces(game_state: GameState, piece: str) -> int:
    return reduce(lambda acc, i: acc + 1 if i == piece else acc, flatten(game_state), 0)


# given a column and a row determines whether it is empty
def is_cell_empty(game_state: List[List[str]], column: int, row: int) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    return 0 <= column < dimensions_x and 0 <= row < dimensions_y and game_state[row][column] is None


# checks overall game_state validity via three other functions.
def is_state_valid(game_state: GameState) -> bool:
    return are_amount_of_pieces_valid(game_state) \
           and not are_there_pieces_with_empty_spots_below(game_state) \
           and not are_there_invalid_pieces(game_state)
