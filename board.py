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



class Board:
    def __init__(self, game):
        self.xsize = 10000
        self.ysize = constants.HEIGHT
        self.game = game
        for i in range(0, self.ysize, 32):
            wall.Wall(game, i, constants.HEIGHT-32)
        spikes.Spike(game, 64, constants.HEIGHT-48)

    def parse(self, name):
        #first delete all spike and wall objects
        for o in self.game.objects:
            if isinstance(o, wall.Terrain):
                self.game.objects.remove(o)
        with open(name) as f:
            for l in f:
                d = [int(x) for x in l.split()]
                {0: wall.Wall,
                 1: spikes.Spike}[d[0]](self.game, d[1], d[2])
