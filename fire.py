import random
import pygame
import time
import sys
import math
import constants
import sprite

class Fire(sprite.Sprite):
    def __init__(self, game, x, y, vx, vy):
        super(Fire, self).__init__(game)
        self.x = x
        self.y = y
        self.vx = vx/3 + (random.random() - .5)
        self.vy = vy/3 + (random.random() - .5)
        self.hp = self.maxhp = 20
        self.img = pygame.image.load('imgs/exhaust.png').convert_alpha()

    def tick(self):
        self.x += self.vx
        self.y += self.vy
        self.hp -= 1
        return self.hp <= 0

    def draw(self):
        self.rect = pygame.Rect(self.x-16-self.game.player.viewx1, 
                                self.y-16, 32, 32)
        n = pygame.Surface((32, 32), pygame.SRCALPHA, 32)
        m = self.img.copy()
        n.fill((127, 127*self.hp/self.maxhp, 0, 127))
        n.set_alpha(127)
        m.blit(n, (0,0), special_flags=pygame.BLEND_RGB_MIN)
        self.game.screen.blit(m, self.rect, special_flags = pygame.BLEND_ADD)

