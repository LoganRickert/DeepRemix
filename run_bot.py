from game import Game


devkey = '58268225b642e9d038e35c52'
username = 'charlieyou'
# devkey = '582632dd3c0cc0ed06f9d05a'
# username = 'mxms'

if __name__ == '__main__':
    gg = Game(devkey, username, practice=True, local=True)
    # tt = gg.board.findMove(gg)
