from game import Game
from bots import QualifierBot

devkey = '58268225b642e9d038e35c52'
username = 'charlieyou'
# devkey = '582632dd3c0cc0ed06f9d05a'
# username = 'mxms'

if __name__ == '__main__':
    game = Game(devkey, username, practice=True, local=True)
    bot = QualifierBot(game.state)

    while not game.state.completed:
        move = bot.get_move(game.state)
        game.submit_move(move)
