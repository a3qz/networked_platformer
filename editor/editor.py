import random
import time
import data
import sprite
import sys
import pygame
import constants
import collectable
import client
import wall
from struct import *
import board

class Game:
    def __init__(self, s):
        self.objects = []
        self.screen = s
        self.player = Ship(self, 100, 100, "91913")
        self.bigfont = pygame.font.Font("./fonts/megaman_2.ttf", 32)
        self.board = board.Board(self)
        self.board.parse("./levels/beta.lvl")

    def tick(self):
        self.player.tick()

    def draw(self):
        self.screen.fill(constants.GREEN)
        for b in reversed(self.objects):
            b.draw()

    def handleKeyDown(self, k):
        self.player.handleKeyDown(k)
    def handleKeyUp(self, k):
        self.player.handleKeyUp(k)
    def handleMUP(self, xxt, yyt):
        self.player.handleMUP(xxt, yyt)
    def handleMDOWN(self, xxt, yyt, event):
        x = int((16 + xxt - self.player.view[0])/32)*32
        y = int((16 + yyt - self.player.view[1])/32)*32
        if event.button == 1:
            self.board.ref[int(self.player.toadd)](self, x, y,
                    int(self.player.toadd))
        else:
            rect = pygame.Rect(0, 0, 1, 1)
            l1 = self.objects
            l2 = [w.rect for w in l1]
            i = rect.move(x, y).collidelist(l2)
            if i != -1:
                self.objects = [o for o in self.objects if o != l1[i]]  
 
class Ship(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Ship, self).__init__(game)
        self.rect.move_ip(x, y)
        self.img = pygame.image.load('imgs/cards/smaller_pngs/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.view = (0, 0)
        self.toadd = ''
        self.rect.inflate_ip(100, 145)
        self.keys = 0

    def tick(self):
        self.rect.move_ip(self.vx, self.vy)
        self.view = (constants.WIDTH/2 - self.rect.x,
                     (constants.HEIGHT*3)/4 - self.rect.y)

        self.fly()

    def draw(self):
        self.game.screen.blit(self.img, self.rect.move(*self.view))
        label = self.game.bigfont.render(self.toadd, 1, (255, 255, 255))
        self.game.screen.blit(label, (10, 10))
        
    def handleKeyDown(self, k):
        if k == 'a':
            self.keys |= 1
        elif k == 'd':
            self.keys |= 2
        elif k == 'w':
            self.keys |= 4
        elif k == 's':
            self.keys |= 8
        elif k.isdigit() and len(k) == 1:
            self.toadd = self.toadd + k
        elif k == 'backspace':
            self.toadd = self.toadd[:-1]

    def handleKeyUp(self, k):
        if k == 'a':
            self.keys &= ~1
        elif k == 'd':
            self.keys &= ~2
        elif k == 'w':
            self.keys &= ~4
        elif k == 's':
            self.keys &= ~8

    def fly(self):
        self.vx = (((self.keys & 2)>>1) - ((self.keys & 1)>>0)) *  7
        self.vy = (((self.keys & 4)>>2) - ((self.keys & 8)>>3)) * -7

    def handleMDOWN(self, xxt, yyt):
        self.firing = True

    def handleMUP(self, xxt, yyt):
        self.firing = False
