from game import Game

devkey = '582632dd3c0cc0ed06f9d05a'
username = 'mxms'

if __name__ == '__main__':
    gg = Game(devkey, username, True)
    tt = gg.board.findMove(gg)
