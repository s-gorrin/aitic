"""
An implementation of a tic-tac-toe game.
It can be played by humans or by AI tic-tac-toe bots.

@author Seth Gorrin
"""


class TicTacToe:

    OUTCOMES = ('player O wins', 'player X wins', 'draw', 'in progress')
    PLAYER_ONE = 'X'
    PLAYER_TWO = 'O'
    EMPTY = '-'
    SPOTS = {1: (0, 0), 2: (0, 1), 3: (0, 2),
             4: (1, 0), 5: (1, 1), 6: (1, 2),
             7: (2, 0), 8: (2, 1), 9: (2, 2)}

    def __init__(self):
        self.board = [[self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY],
                      [self.EMPTY, self.EMPTY, self.EMPTY]]

        self.move_count = 0
        self.outcome = self.OUTCOMES[3]

    def print_board(self):
        for r in self.board:
            for item in r:
                print(item, end=" ")
            print()

    def at(self, spot):
        """
        Get a location on the board by number.
        Results are not assignable.
        """
        return self.board[self.SPOTS[spot][0]][self.SPOTS[spot][1]]

    def symbol(self, flip=0):
        """
        Get the correct symbol for the current player.

        flip: flip the result if needed, generally for printing outside the class
        :return: The player symbol
        """
        if flip != 0:
            flip = 1
        if self.move_count % 2 == flip:
            return self.PLAYER_TWO
        return self.PLAYER_ONE

    def make_move(self, move):
        """
        Make a tic-tac-toe move.

        :param move: the number of the move to make
        :return: True if move was made, False if not
        """
        # check if game is already over
        if self.outcome is not self.OUTCOMES[3]:
            return False
        # convert move by number to coordinates
        if move not in range(1, 10):
            return False
        move_row, move_col = self.SPOTS[move][0], self.SPOTS[move][1]
        # check for out of bounds moves
        if not 0 <= move_row <= 2 or not 0 <= move_col <= 2:
            return False
        if self.board[move_row][move_col] == '-':
            self.move_count += 1
            self.board[move_row][move_col] = self.symbol()
            # check for outcomes after move is made
            # the earliest possible win is move 5
            if self.move_count >= 4 and self.is_win():
                self.outcome = self.OUTCOMES[self.move_count % 2]
            elif self.move_count == 9:  # last move has been played, and it was not a win
                self.outcome = self.OUTCOMES[2]
            return True
        return False

    def is_win(self):
        """
        Check the board for wins.

        precondition 1: board is a 3x3 tic-tac-toe board represented as a 2d list
        precondition 2: symbol is either 'X' or 'O', representing player pieces
        :return: true if player has won, false if not
        """
        symbol = self.symbol()  # which player's symbol to check for
        win = False
        # check rows for wins
        for r in self.board:
            if r.count(symbol) == 3:
                win = True
        # check columns for wins
        for c in range(3):
            if [self.board[0][c], self.board[1][c], self.board[2][c]].count(symbol) == 3:
                win = True
        # check diagonals for wins
        if [self.board[0][0], self.board[1][1], self.board[2][2]].count(symbol) == 3:
            win = True
        if [self.board[0][2], self.board[1][1], self.board[2][0]].count(symbol) == 3:
            win = True
        return win

    def reset(self):
        """
        Reset the game to play again.
        """
        self.__init__()


# play tic-tac-toe as a human
if __name__ == '__main__':
    game = TicTacToe()
    while game.outcome == TicTacToe.OUTCOMES[3]:
        legal = False
        while not legal:
            move_number = input(f"enter move for {game.symbol(1)}: ")
            legal = game.make_move(int(move_number))
            game.print_board()
    print(game.outcome)
