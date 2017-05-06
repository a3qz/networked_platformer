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
import spikes


class Shadow(sprite.Sprite):
    def __init__(self, game, uid):
        super(Shadow, self).__init__(game)
        self.img = pygame.image.load('imgs/cards/pngs/player.png').convert_alpha()

        self.uid = uid
        self.height = 145

    def draw(self):
        rect = pygame.Rect(self.x-self.game.player.viewx1-60, self.y-145, 120, 120)
        mouse = pygame.mouse.get_pos()
        angle = 180-math.degrees(math.atan2(self.y - mouse[1],
            self.x - mouse[0] - self.game.player.viewx1))
        rot_image = pygame.transform.rotate(self.img, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        self.game.screen.blit(self.img, rect)

    def tick(self):
        self.x += self.vx
        w = self.thing_at(wall.Wall, 32, 32, 0, 0) or (
            self.thing_at(Ship, 50, 0, -50, -145) or (
            self.thing_at(Shadow, 50, 0, -50, -145)))
        if w:
            self.y = w.y - w.height
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
        self.x = self.xstart = x
        self.y = self.ystart = y
        self.viewx1 = self.x-constants.WIDTH/2
        self.viewx2 = self.x+constants.WIDTH/2
        self.height = 145
        self.keys = 0
        self.img = pygame.image.load('imgs/cards/pngs/player2.png').convert_alpha()
        self.firing = False
        self.dead_ticks = 0

    def gotoDead(self):
        self.dead_ticks = constants.DEAD_TIME

    def tick(self):
        if self.dead_ticks > 0:
            self.dead_ticks -= 1
            self.x = 300
            self.y = 4444
            if self.dead_ticks == 0:
                self.x = self.xstart
                self.y = self.ystart
            return False

        self.x += self.vx
        w = self.thing_at(wall.Wall, 32, 32, 0, 0) or (
            self.thing_at(Shadow, 50, 0, -50, -145))
        if w:
            self.y = w.y - w.height
            self.vy = 0
            if ((self.keys & 4)>>2) > 0:
                self.vy = -20
                self.y -= 1
        else:
            self.y += self.vy
            self.vy += 1
            if self.vy > 12:
                self.vy = 12

        w = self.thing_at(spikes.Spike, 32, 32, 0, 0)
        if self.y > constants.HEIGHT*1.5 or w:
            self.gotoDead()

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
