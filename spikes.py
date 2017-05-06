import random
import pygame
import time
import sys
import math
import fire
import sprite
import wall

class Spike(wall.Terrain):
    def draw(self):
        xx = self.game.player.viewx1
        points = [(-16, 16),
                  (-8, -16),
                  (0, 16),
                  (8, -16),
                  (16, 16)]
        pygame.draw.lines(self.game.screen, (120, 120, 120), True,
                         [(self.x+x[0]-xx, self.y+x[1])for x in points], 1)

