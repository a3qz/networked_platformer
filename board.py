import spikes
import wall
import constants
import collectable
import data



class Board:
    def __init__(self, game):
        self.xsize = 10000
        self.ysize = constants.HEIGHT
        self.game = game
        # create a reference dict for the parser based off of the json dicts of cards + the wall and spikes
        self.ref = {
                0: wall.Wall,
                 1: spikes.Spike
                 }
        for i in data.num_as_key:
            self.ref[int(i)] = collectable.Collectable
        # failsafe walls
        for i in range(0, self.ysize, 32):
            wall.Wall(game, i, constants.HEIGHT-32, 0)

    # interpret a file
    def parse(self, name):
        #first delete all spike and wall objects
        self.game.objects = [o for o in self.game.objects 
                             if (not isinstance(o, wall.Terrain)) and
                                (not isinstance(o, collectable.Collectable))]
        #iterate through the file and separate into [type, xcoord, ycoord]
        with open(name) as f:
            for l in f:
                d = [int(x) for x in l.split()]
                # find the item in the reference dictionary and call its constructor
                self.ref[d[0]](self.game, d[1], d[2], d[0])
        # create the "bottom" of the level, where the player dies
        self.game.deathzone = max([o.rect.y
                                   for o in self.game.objects
                                   if isinstance(o, wall.Wall)]) + 200
    def save(self, name):
        #first delete all spike and wall objects
        d = ['{} {} {}\n'.format(o.descriptor, o.rect.centerx, o.rect.centery)
             for o in self.game.objects 
             if (isinstance(o, wall.Terrain)) or
                (isinstance(o, collectable.Collectable))]
        #writes lines to the temp file
        with open(name, 'w') as f:
            f.writelines(d)
