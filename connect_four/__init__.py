import typing

GameState = typing.List[typing.List[typing.Union[None, str]]]
player = str


def init_game_state(size_y: int, size_x: int) -> GameState:
    return [[None for _ in range(size_x)] for _ in range(size_y)]
