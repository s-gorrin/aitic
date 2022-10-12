# play the game
from tic_tac_toe import TicTacToe as Ttt
from aitic import AItic

game = Ttt()
bot_one = AItic(Ttt.PLAYER_ONE, game)
bot_two = AItic(Ttt.PLAYER_TWO, game)

for i in range(100):
    while game.outcome == Ttt.OUTCOMES[3]:
        bot_one.play()
        if game.outcome != Ttt.OUTCOMES[3]:
            break
        bot_two.play()

    print(f"game {i}:")
    game.print_board()
    bot_one.game_over(game.outcome)
    bot_two.game_over(game.outcome)
    game = Ttt()
    bot_one.new_game(game)
    bot_two.new_game(game)

print("weights after games:")
print("bot one:", bot_one.weighted_moves)
print("bot two:", bot_two.weighted_moves)
