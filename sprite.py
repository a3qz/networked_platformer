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
        self.width = 0
        self.height = 0
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

    def thing_at(self, c, x1, y1, x2, y2):
        for w in self.game.objects:
            if isinstance(w, c) and self != w:
                if self.x < w.x + x2: continue
                if self.x > w.x + x1: continue
                if self.y < w.y + y2: continue
                if self.y > w.y + y1: continue
                return w
        return None
