from game import Game
from bots import QualifierBot

#devkey = '58268225b642e9d038e35c52'
#username = 'charlieyou'
devkey = '58343b88dd23e7896bf06c01'
username = 'mxms'

if __name__ == '__main__':
    game = Game(devkey, username, practice=True, local=False)
    bot = QualifierBot(game.state)

    while not game.state.completed:
        moves = bot.get_move(game.state)
        
        print "MAKING MOVES " + repr(moves)
        
#        for move in moves:
        game.submit_move(moves)
