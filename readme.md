# Brian Yeh - Comments

Thanks Brice for this assignment. I wrote two functions for manual QA: a 
game loop function and a game state display function. You can run this 
with python 3.6 by executing main.py in the root directory. 

I wrote all the code in a purely functional style with type annotations using
the pycharm IDE to catch all type errors. FYI I don't use this style of programming at work
as purely functional programming is not considered pythonic and is an unconventional
and less readable style. However, due to the freedom given in this assignment and 
given the fact that I truly believe that this style allows for the building of 
better programs with less bugs so I went with it. There is a slight cost of using 
the functional style in that it is less efficient then imperative programming. 
The biggest slowdown would be in recreating the game_state on every update.   

Overall there were 3 main stages in writing this program which I used to filter
out as many bugs as possible. 

1. The first stage was to just code it using a functional style and type annotations.
This step eliminates possibly 80% of bugs due to the style itself. I followed the 
philosophy exemplified here: https://wiki.haskell.org/Why_Haskell_just_works 

2. The second stage was to write unit tests for all the functions. Pure functional
programming segments your code into many tiny micro functions allowing for in depth 
and thorough coverage of every aspect of the program. The coding style of the tests was 
imperative and due to that I spend 10x more time fixing bugs within the tests itself then
I did with the actual program. 

3. Write a program that plays the game. This allows me to run a manual end to end 
test and catch any remaining bugs. If at any point I catch a bug I go back to step 2
implement a unit test for it and continue. 




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
