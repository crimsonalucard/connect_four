from typing import List, Any
from platform import system as system_name
from os import system as system_call


# flattens a list of lists into a single list.
def flatten(list_of_lists: List[List[Any]]):
    return [item for sublist in list_of_lists for item in sublist]


# clears the screen
def clear_screen():
    """
    Clears the terminal screen.
    """

    # Clear command as function of OS
    command = "-cls" if system_name().lower() == "windows" else "clear"

    # Action
    system_call(command)
