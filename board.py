import spikes
import wall
import constants



class Board:
    def __init__(self, game):
        self.xsize = 10000
        self.ysize = constants.HEIGHT
        self.game = game
        for i in range(0, self.ysize, 32):
            wall.Wall(game, i, constants.HEIGHT-32)

    def parse(self, name):
        #first delete all spike and wall objects
        self.game.objects = [o for o in self.game.objects 
                             if not isinstance(o, wall.Terrain)]
        with open(name) as f:
            for l in f:
                d = [int(x) for x in l.split()]
                {0: wall.Wall,
                 1: spikes.Spike}[d[0]](self.game, d[1], d[2])
