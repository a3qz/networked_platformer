import random
import pygame
import time
import sys
import math
import bullet
import fire

class Sprite(object):
    def __init__(self, game):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.game = game
        game.objects.append(self)

    def tick(self):
        self.x += self.vx
        self.y += self.vy
        
    def draw(self):
        pass

    def die(self):
        pass
