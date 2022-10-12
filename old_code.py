"""
AItic: how to learn to play tic tac toe

board:
0 1 2
3 4 5
6 7 8

move options (keys for moves dict and weights dict):
 - the dict that stores the following is called weighted_moves
first empty
second empty
third empty
fourth empty
fifth empty
sixth empty
seventh empty
eighth empty
ninth empty
win
stop opponent win
set up win (this is bonus)

1: look at the board
    create a dict of key value pairs where the keys are possible moves
    and the values are the corresponding number on the board
    this is two steps:
    a: first is identifying if a move options is present from weighted_moves.keys()
        for example, if a given direction has 2*X and 1*empty, that's a 'win'
    b: next, figure out which square number is the thing. The first part
        can return the row/col/dia that has the win on it, and the second
        part checks the three squares to find the number
    c: the number it found becomes the move for the dict: {'win': move}
    d: this goes into a dict called "this_turn" or something
2: generate possible moves dict with keys from 1 and weights from storage table
    a: for key in this_turn.keys() (or whatever python syntax)
    b: possible_moves[key] = weighted_moves[key]
3: pick a move from dict in 2, with higher weights having higher priority
    maybe shuffle order and then give each move a chance with weight/100
    randomly selected so: r = rand(0-100), if r < weight, play the move
4: take selected move as key and find its value in dict from 1
5: add the move to a list of moves played this game, then play the move
    a: played_moves.add(move) where move is by identifier, not number on board
6: repeat until game is over
7: if game is a win, each move in the played_moves list gets +1 in
    the big weights table (weighted_moves)
    if game is a loss, each move gets -1
8: play again

"""
from tic_tac_toe import TicTacToe as ttt

# dummy functions to stand in for tasks as describes

# return the board b as a 2D list, rotated r places
def rotations(b, r):
    """
    small example, r = 1:
    [[a, b], ->  [[c, a],
     [c, d]] ->   [d, b]]
    """
    return b


# return true if a real board matches a reference-formatted board
# with Xs in the right places, empty squares where indicated,
# and M is a legal move
def match(real, ref):
    return real == ref


# first "lesson" of Part 1
W = 'wildcard'  # irrelevant squares (for the given 'lesson')
E = 'empty'  # explicitly empty squares
M = 'current move'  # move to make
X = 'past move'  # existing moves that have been made

# This list defines moves which lead to wins on the following move, but ignore possible opponent wins.
# It is assumed that elsewhere in the code, it allows for rotations of these options.
# Either by rotating, or by always orienting off existing moves in some way.
# boards are numbered to make it easier to see where they start in a wall of list
win_next_move = [[[X, E, M],  # 1
                  [W, W, E],
                  [W, W, X]],
                 [[E, X, M],  # 2
                  [W, W, X],
                  [W, W, E]],
                 [[W, X, W],  # 3
                  [E, M, X],
                  [W, E, W]],
                 [[W, W, X],  # 4
                  [E, X, M],
                  [W, W, E]],
                 [[E, M, X],  # 5
                  [W, X, W],
                  [W, E, W]],
                 [[W, W, X],  # 6
                  [X, M, E],
                  [E, W, W]],
                 [[W, E, X],  # 7
                  [W, M, W],
                  [E, X, W]]]


# second "lesson" of Part 1
# identify a possible win on the current move
# if so, return the row, column, or diagonal to win on
def win_possible(real_board, player):
    possible = False
    for i in range(3):
        if real_board[i].count(player) == 2:
            possible = True
        if [real_board[0][i], real_board[1][i], real_board[2][i]].count(player) == 2:
            possible = True
    if [real_board[0][0], real_board[1][1], real_board[2][2]].count(player):
        possible = True
    elif [real_board[0][2], real_board[1][1], real_board[2][0]].count(player):
        possible = True
    return possible


def set_up_win(ai, real_board):
    if win_possible(real_board, 'X'):
        ai.win()  # instruct AI to find the win
    if win_possible(real_board, 'O'):
        ai.stop_loss()  # instruct AI to stop opponent's win if possible
    # try and set up a winning position if possible
    for board in win_next_move:
        for r in range(4):
            rotated_board = rotations(board, r)  # a function that rotates the reference board
            if match(real_board, rotated_board):
                ai.move(rotated_board)  # provide reference board for AI to base a move on

    ai.move()  # default move, just try to move well based on other criteria


