import random
import pygame
import time
import sys
import math
import sprite

class Terrain(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Terrain, self).__init__(game)
        self.rect.move_ip(x, y)
        self.rect.inflate_ip(32, 32)

    def tick(self):
        return False

    
class Wall(Terrain):
    def __init__(self, game, x, y, descriptor):
        super(Wall, self).__init__(game, x, y, descriptor)
        self.descriptor = "0"

    def draw(self):
        pygame.draw.rect(self.game.screen, (255, 255, 255),
                         self.rect.move(*self.game.player.view), 1)

