import random
import pygame
import time
import sys
import math
import sprite
import wall

# class for the spikes that hurt
class Spike(wall.Terrain):
    def __init__(self, game, x, y, descriptor):
        super(Spike, self).__init__(game, x, y, descriptor)
        self.descriptor = "1"

    # render the lines in a triangle 
    def draw(self):
        xx = self.game.player.view[0]
        yy = self.game.player.view[1]
        points = [(0, 32),
                  (8, 0),
                  (16, 32),
                  (24, 0),
                  (32, 32)]
        # draw the lines to form the points
        pygame.draw.lines(self.game.screen, (255, 255, 255), True,
                         [(self.rect.x+x[0]+xx, self.rect.y+x[1]+yy)
                          for x in points], 1)

