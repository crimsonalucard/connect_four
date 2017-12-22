from connect_four import GameState


# checks downward for a left diagonal
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


# checks downward for a right diagonal
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


# checks down for a vertical row
def is_n_in_a_vertical_row(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    dimensions_y: int = len(game_state)
    dimensions_x: int = len(game_state[0])
    if column < 0 or column >= dimensions_x or row < 0 or row >= dimensions_y:
        return False
    elif n == 1:
        return game_state[row][column] == piece
    else:
        return game_state[row][column] == piece and is_n_in_a_vertical_row(game_state, n - 1, column, row + 1, piece)


# checks left for a horizontal row
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


# checks every direction downward for a n in a row
def is_n_in_a_row(game_state: GameState, n: int, column: int, row: int, piece: str) -> bool:
    return is_n_in_a_horizontal_row(game_state, n, column, row, piece) or \
           is_n_in_a_vertical_row(game_state, n, column, row, piece) or \
           is_n_in_a_diag_row_right(game_state, n, column, row, piece) or \
           is_n_in_a_diag_row_left(game_state, n, column, row, piece)
