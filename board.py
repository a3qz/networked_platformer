import random
import pygame
import time
import sys
import math
import bullet
import spikes
import fire
import sprite
import wall
import constants
import collectable
import data



class Board:
    def __init__(self, game):
        self.xsize = 10000
        self.ysize = constants.HEIGHT
        self.game = game
        self.ref = {
                0: wall.Wall,
                 1: spikes.Spike
                 }
        for i in data.num_as_key:
            self.ref[int(i)] = collectable.Collectable
        for i in range(0, self.ysize, 32):
            wall.Wall(game, i, constants.HEIGHT-32, 0)

    def parse(self, name):
        #first delete all spike and wall objects
        self.game.objects = [o for o in self.game.objects 
                             if not isinstance(o, wall.Terrain)]
        with open(name) as f:
            for l in f:
                d = [int(x) for x in l.split()]
                self.ref[d[0]](self.game, d[1], d[2], d[0])
