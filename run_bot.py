from game import Game
from bots import MCTSBot

devkey = '58343b88dd23e7896bf06c01'
username = 'mxms'

if __name__ == '__main__':
    game = Game(devkey, username, practice=True)
    bot = MCTSBot(game.state, game.state.player.id, sim_time=10)

    while not game.state.completed:
        move = bot.get_move(game.state)
        print "MAKING MOVE " + repr(move)
        game.submit_move(move)
