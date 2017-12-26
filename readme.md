# Brian Yeh - Comments

Thanks Brice for this assignment. 
I wrote two functions for manual QA: a game loop function and a game state display function. You can run this 
with python 3.6 by executing main.py in the root directory. 

You can run the unit tests by running run_tests.sh (also in the root directory.) 

type annotations are used for everything except tests. Run 'mypy main.py' to verify type
correctness. 

The is_state_valid function is the most expensive and complex function. I went through 2 different
versions of this function during development. The initial version although O(n) will not find 
all invalid configurations of game_state. The second version of that function is more robust
(please see comment above the is_state_valid function for more info on it) but slower. You will
see the obsolete is_game_state and support functions moved to the file obsolete_functions.py  

# Connect Four

The animation demonstrates Connect Four gameplay where the first player begins
by dropping his/her yellow disc into the center column of the game board. The
two players then alternate turns dropping one of their discs at a time into an
unfilled column, until the second player, with red discs, achieves four discs
in a row, diagonally, and wins. If the game board fills before either player
achieves four in a row, then the game is a draw.


![Connect Four
](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Connect_Four.gif/220px-Connect_Four.gif)


## Expectations

It can be assumed that the candidate knows the rules and culprits of the
Connect Four game. State based logic is simpler to test, the candidate is
expected to heavily rely on testing.

## Game State

The connect four state of the game is represented as a two dimensional array.
After every turn, this state is updated.

```python
game_state = [
  [None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None],
  [None, None, "y", "r", None, None, None],
  [None, None, "r", "y", None, None, None],
  ["r", "y", "y", "y", "r", "r", "y"],
  ["r", "r", "y", "y", "r", "y", "r"],
]
```

## Who's turn is it?

Write a method which, given a game state, returns which player is
supposed to play next. The return value is a string,
either "y" (for the yellow player) or "r" (for the red player).

```python
>>> get_current_player(game_state)
"y"
```

## Assert state integrity

Write a method which detects anomalies in a given state. The return
value is a boolean and should return `True` when the state is valid.


```python
>>> is_state_valid(game_state)
True
```


## Play

Write a play method which accept a state, a column and a color and return
a new game state.

The column argument should accept a value between 0, and 6 (there is 7 columns
in a connect four game)

```python
>>> game_state = [
...   [None, None, None, None, None, None, None],
...   [None, None, None, None, None, None, None],
...   [None, None, "y", "r", None, None, None],
...   [None, None, "r", "y", None, None, None],
...   ["r", "y", "y", "y", "r", "r", "y"],
...   ["r", "r", "y", "y", "r", "y", "r"],
... ]
>>> play(game_state, 1, "y")
[
  [None, None, None, None, None, None, None],
  [None, None, None, None, None, None, None],
  [None, None, 'y', 'r', None, None, None],
  [None, 'y', 'r', 'y', None, None, None],
  ['r', 'y', 'y', 'y', 'r', 'r', 'y'],
  ['r', 'r', 'y', 'y', 'r', 'y', 'r']
]
```

## Winner

Create a function which, given a game state, returns `True` if the game
has a winner.
