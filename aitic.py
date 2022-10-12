import random

from tic_tac_toe import TicTacToe as Ttt
from tic_tac_toe import to_spot


def init_weights():
    """
    Set up the initial values of the weight table
    """
    return {'0': 5,
            '1': 5,
            '2': 5,
            '3': 5,
            '4': 5,
            '5': 5,
            '6': 5,
            '7': 5,
            '8': 5,
            'win': 90,
            'prevent win': 50}


def find(needle, haystack):
    for i in range(len(haystack)):
        if haystack[i] == needle:
            return i
    return False


class AItic:

    def __init__(self, symbol, current_game):
        """
        :param symbol: player symbol
        :param current_game:   the current game
        """
        self.symbol = symbol
        self.opponent = [s for s in (Ttt.PLAYER_ONE, Ttt.PLAYER_TWO) if s != symbol][0]
        self.weighted_moves = init_weights()
        self.moves_this_turn = {}
        self.weighted_this_turn = {}
        self.moves_this_game = []
        self.game = current_game

    def new_game(self, current_game):
        self.moves_this_turn = {}
        self.weighted_this_turn = {}
        self.moves_this_game = []
        self.game = current_game

    def find(self, needle, haystack):
        for s in haystack:
            if self.game.at(s) == needle:
                return s
        return False

    def check_special(self, span):
        """
        Check a span for special moves.
        If the span has two of the same player symbol and one empty spot,
            then a special thing is present. Return the board spot of that thing.
        """
        win, prevent_win = False, False
        board_span = [self.game.at(span[0]), self.game.at(span[1]), self.game.at(span[2])]
        if board_span.count(Ttt.EMPTY) == 1:
            if board_span.count(self.symbol) == 2:
                win = self.find(Ttt.EMPTY, span)
            elif board_span.count(self.opponent) == 2:
                prevent_win = self.find(Ttt.EMPTY, span)
        return win, prevent_win

    def analyze_specials(self):
        """
        Analyze the board for special moves.
        """
        win = False
        prevent_win = False
        # check rows
        for r in range(0, 7, 3):
            # row = [self.game.at(r), self.game.at(r + 1), self.game.at(r + 2)]
            row = [r, r + 1, r + 2]
            win, prevent_win = self.check_special(row)
        # check columns
        for c in range(3):
            # col = [self.game.at(c), self.game.at(c + 3), self.game.at(c + 6)]
            col = [c, c + 3, c + 6]
            if not win:
                win = self.check_special(col)[0]
            if not prevent_win:
                prevent_win = self.check_special(col)[1]
        # check diagonals
        # dig = [self.game.at(0), self.game.at(4), self.game.at(8)]
        dig = [0, 4, 8]
        if not win:
            win = self.check_special(dig)[0]
        if not prevent_win:
            prevent_win = self.check_special(dig)[1]
        # dig = [self.game.at(2), self.game.at(4), self.game.at(6)]
        dig = [2, 4, 6]
        if not win:
            win = self.check_special(dig)[0]
        if not prevent_win:
            prevent_win = self.check_special(dig)[1]
        print(f"specials found? win: {win}, prevent: {prevent_win}")
        return win, prevent_win

    def analyze_board(self):
        """
        Analyze the board to make a dict of playable moves by name and their numbers.
        """
        win, prevent_win = self.analyze_specials()
        empties = []
        # generate list of empty spots in the board
        print("spots: ", end="")
        for spot in range(len(Ttt.SPOTS)):
            print(spot, end=" ")
            if self.game.at(spot) == Ttt.EMPTY:
                if win is spot or prevent_win is spot:  # avoid duplicate entries
                    pass
                else:
                    empties.append(spot)
        print(f"\nbot empties: {empties}")
        names = [k for k in sorted(self.weighted_moves.keys())
                 if k != 'win' and k != 'prevent win' and k < str(len(empties))]
        # generate a dictionary of moves that are playable this turn
        # in the format {weighted_move_name: tic-tac-toe move}
        moves = dict(zip(names, empties))
        if win:
            moves['win'] = win
        if prevent_win:
            moves['prevent win'] = prevent_win
        self.moves_this_turn = moves

    def weight_moves(self):
        self.weighted_this_turn.clear()
        print(f"bot moves this turn: {self.moves_this_turn}")
        for move in self.moves_this_turn.keys():
            self.weighted_this_turn[move] = self.weighted_moves[move]

    def pick_move(self):
        """
        Generate a list of possible moves where each move gets added its weight times.
        Pick randomly from that list, such that higher-weight moves have higher chance of being picked.
        This is where the AI choice happens, with moves_this_turn being the state.
        """
        # this weighted selection is likely not optimal
        # it may be better to attempt each move in order of best to worst:
        # weights are in the form 0-1, where 1 is always played and 0 is never played
        # and a move is selected with a random number 0-1, and the move is played
        #  if the random number is less than the weight
        weighted_list = []
        for key in self.weighted_this_turn.keys():
            for i in range(self.weighted_this_turn[key]):
                weighted_list.append(key)
        move = random.choice(weighted_list)
        print(f"bot picks {move}")
        self.moves_this_game.append(move)  # track moves played this game
        self.game.make_move(self.moves_this_turn[move])

    def play(self):
        self.analyze_board()
        self.weight_moves()
        self.pick_move()

    def game_over(self, outcome):
        if (self.symbol == Ttt.PLAYER_ONE and outcome == Ttt.OUTCOMES[1]) or \
                (self.symbol == Ttt.PLAYER_TWO and outcome == Ttt.OUTCOMES[0]):  # win
            for value in self.weighted_moves:
                value += 1
        elif outcome == Ttt.OUTCOMES[2]:  # draw
            pass
        else:  # lose
            for value in self.weighted_moves:
                value -= 1


if __name__ == '__main__':
    game = Ttt()
    bot = AItic(Ttt.PLAYER_ONE, game)
    while game.outcome == Ttt.OUTCOMES[3]:
        bot.play()
        game.print_board()
        if game.outcome != Ttt.OUTCOMES[3]:
            break
        human = input("play a move: ")
        game.make_move(int(human))
