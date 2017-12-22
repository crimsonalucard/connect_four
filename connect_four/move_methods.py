from connect_four import GameState
from connect_four.game_validity_checkers import is_move_valid, is_cell_empty, is_game_valid


# place a piece at a column.
def place_piece(game_state: GameState, piece: str, column: int) -> GameState:
    row: int = find_valid_empty_row(game_state, column)
    return update_game_state(game_state, piece, column, row) if \
        is_game_valid(game_state) and is_move_valid(game_state, column, row) else game_state


# update the game state by copying it. O(n) due to game_state being immutable.
def update_game_state(game_state: GameState, piece: str, column: int, row: int) -> GameState:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    return [[piece if j == column and i == row else game_state[i][j] for j in range(dimensions_x)] for i in
            range(dimensions_y)]


# find the correct row the piece will land into when dropped at a column
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
