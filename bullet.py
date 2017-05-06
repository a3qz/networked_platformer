import random
import pygame
import time
import sys
import math
import constants
import fire
import enemy
import sprite

class Bullet(sprite.Sprite):
    def __init__(self, game, x, y, vx, vy):
        super(Bullet, self).__init__(game)
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.game = game
        self.hp = 2

    def enemycollide(self):
        for e in [i for i in self.game.objects if isinstance(i, enemy.Enemy)]:
            if e.rect.collidepoint(self.x, self.y):
                ret = e.img.get_at((
                       int(self.x - e.x) + 60,
                       int(self.y - e.y) + 60
                       )).a > 10
                if ret:
                    e.hurt(1)
                    return True
        return False

    def tick(self):
        while self.x < constants.WIDTH and self.x > 0 and self.y < constants.HEIGHT and self.y > 0 and not self.enemycollide():
            self.x += self.vx
            self.y += self.vy
        self.hp -= 1
        return self.hp <= 0
    
    def draw(self):
        pygame.draw.line(self.game.screen, (255, 0, 0),
                (self.x, self.y), (self.game.player.x, self.game.player.y))

    def die(self):
        fire.Fire(self.game, self.x, self.y, 0, -2)
