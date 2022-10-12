# AItic
### A python tic-tac-toe implementation and a reinforcement learning AI to play it
This project is part of an assignment for Boston University MET CS 664, which is the
source of the name AItic.


## TicTacToe
The game is simple. There are two players, and they alternate
making moves by entering the number of the square the want to
play on. The numbers start with 1 in the top left like so:
```
1 2 3
4 5 6
7 8 9
```

## AItic
The AI is created with its game symbol as input, X or O,
which can be accessed through the `PLAYER_ONE` and
`PLAYER_TWO` member variables of the TicTacToe class.

Call `play()` to make a move, and call `game_over()`
after a game to make sure the correct backwards propagation
takes place.