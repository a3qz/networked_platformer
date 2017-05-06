import random
import pygame
import time
import sys
import math
import fire
import sprite

class Terrain(sprite.Sprite):
    def __init__(self, game, x, y):
        super(Terrain, self).__init__(game)
        self.y = y
        self.x = x

    def tick(self):
        return False

    
class Wall(Terrain):
    def draw(self):
        pygame.draw.rect(self.game.screen, (120, 120, 120),
                         (self.x - self.game.player.viewx1, self.y, 32, 32), 1)

