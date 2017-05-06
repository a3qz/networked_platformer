import random
import pygame
import time
import sys
import math
import bullet
import fire
import sprite
import constants
import wall


class Shadow(sprite.Sprite):
    def __init__(self, game, uid):
        super(Shadow, self).__init__(game)
        self.img = pygame.image.load('imgs/cards/pngs/player.png').convert_alpha()

        self.uid = uid

    def draw(self):
        rect = pygame.Rect(self.x-self.game.player.viewx1-60, self.y-145, 120, 120)
        mouse = pygame.mouse.get_pos()
        angle = 180-math.degrees(math.atan2(self.y - mouse[1],
            self.x - mouse[0] - self.game.player.viewx1))
        rot_image = pygame.transform.rotate(self.img, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        self.game.screen.blit(self.img, rect)
    def wall_below(self):
        for w in self.game.objects:
            if isinstance(w, wall.Wall):
                if self.x < w.x:      continue
                if self.x > w.x + 32: continue
                if self.y > w.y + 32: continue
                if self.y < w.y:      continue
                return w
        return None

    def tick(self):
        self.x += self.vx
        w = self.wall_below()
        if w:
            self.y = w.y
            self.vy = 0
        else:
            self.y += self.vy
            self.vy += 1
            if self.vy > 12:
                self.vy = 12
        if self.vy < 0:
            fire.Fire(self.game, self.x, self.y, -self.vx, -self.vy)

class Ship(sprite.Sprite):
    def __init__(self, game, x, y):
        super(Ship, self).__init__(game)
        self.x = x
        self.y = y
        self.viewx1 = self.x-constants.WIDTH/2
        self.viewx2 = self.x+constants.WIDTH/2
        self.keys = 0
        self.img = pygame.image.load('imgs/cards/pngs/jack_of_hearts2.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (100, 145))
        self.firing = False

    def wall_below(self):
        for w in self.game.objects:
            if isinstance(w, wall.Wall):
                if self.x < w.x:      continue
                if self.x > w.x + 32: continue
                if self.y > w.y + 32: continue
                if self.y < w.y:      continue
                return w
        return None

    def tick(self):
        self.x += self.vx
        w = self.wall_below()
        if w:
            self.y = w.y
            self.vy = 0
            if ((self.keys & 4)>>2) > 0:
                self.vy = -20
                self.y -= 1
        else:
            self.y += self.vy
            self.vy += 1
            if self.vy > 12:
                self.vy = 12
        self.viewx1 = self.x-constants.WIDTH/2
        self.viewx2 = self.x+constants.WIDTH/2
        if self.vy < 0:
            fire.Fire(self.game, self.x, self.y, -self.vx, -self.vy)

    def draw(self):
        rect = pygame.Rect(self.x-self.viewx1-60, self.y-145, 120, 120)
        mouse = pygame.mouse.get_pos()
        angle = 180-math.degrees(math.atan2(self.y - mouse[1],
            self.x - mouse[0] - self.viewx1))
        rot_image = pygame.transform.rotate(self.img, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        self.game.screen.blit(self.img, rect)
        if self.firing:
            angle = math.radians(angle)
            bvx = math.cos(angle)
            bvy = -math.sin(angle)
            fired = bullet.Bullet(self.game, self.x + bvx*20,
                    self.y + bvy*20, bvx, bvy)
        
    def handleKeyDown(self, k):
        if k == 'a':
            self.keys |= 1
        elif k == 'd':
            self.keys |= 2
        elif k == 'w':
            self.keys |= 4
        elif k == 's':
            self.keys |= 8
        self.fly()

    def handleKeyUp(self, k):
        if k == 'a':
            self.keys &= ~1
        elif k == 'd':
            self.keys &= ~2
        elif k == 'w':
            self.keys &= ~4
        elif k == 's':
            self.keys &= ~8
        self.fly()

    def fly(self):
        self.vx = (((self.keys & 2)>>1) - ((self.keys & 1)>>0)) * 3

    def handleMDOWN(self, xxt, yyt):
        self.firing = True

    def handleMUP(self, xxt, yyt):
        self.firing = False
