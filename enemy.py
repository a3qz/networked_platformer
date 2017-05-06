import random
import pygame
import time
import sys
import math
import fire
import sprite

class Enemy(sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.game = game
        self.img = pygame.image.load('imgs/enemy.png').convert_alpha()
        self.rect = pygame.Rect(self.x-60, self.y-60, 120, 120)
        self.hp = self.maxhp = 100

    def tick(self):
        if self.hp > 0:
            return False
        return True

    def draw(self):
        self.rect = pygame.Rect(self.x-60, self.y-60, 120, 120)
        self.game.screen.blit(self.img, self.rect)
        
    def hurt(self, d):
        self.hp -= d
        if self.hp < 0: self.hp = 0
        n = pygame.Surface((120, 120), pygame.SRCALPHA, 32)
        n.fill((255, 255*self.hp/self.maxhp, 255*self.hp/self.maxhp, 127))
        n.set_alpha(10)
        self.img.blit(n, (0,0), special_flags=pygame.BLEND_RGB_MIN)

    def die(self):
        for i in range(100):
            x = self.x + (random.random()-.5)*60
            y = self.y + (random.random()-.5)*60
            dx = (random.random()-.5)*4
            dy = (random.random()-.5)*4
            fire.Fire(self.game, x, y, dx, dy)

