#! /usr/bin/env python3

from connect_four.game import game_loop
from connect_four import init_game_state

# runs the game loop.
if __name__ == "__main__":
    game_loop(init_game_state(6, 7))
