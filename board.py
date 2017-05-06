import random
import pygame
import time
import sys
import math
import bullet
import fire
import sprite
import wall
import constants



class Board:
    def __init__(self, game):
        self.xsize = 10000
        self.ysize = constants.HEIGHT
        for i in range(0, self.ysize, 32):
            wall.Wall(game, i, constants.HEIGHT-32)




