# play the game
from tic_tac_toe import TicTacToe as Ttt
from aitic import AItic

game = Ttt()
bot = AItic(Ttt.PLAYER_TWO, game)
while game.outcome == Ttt.OUTCOMES[3]:
    game.print_board()
    human = input("play a move: ")
    game.make_move(int(human))
    if game.outcome != Ttt.OUTCOMES[3]:
        break
    bot.play()

game.print_board()
bot.game_over(game.outcome)
print("weights after game:")
print(bot.weighted_moves)
