import random
import pygame
import time
import sys
import math
import data
import fire
import sprite
import constants
import wall
import spikes


class Shadow(sprite.Sprite):
    def __init__(self, game, uid):
        super(Shadow, self).__init__(game)
        self.num = random.randint(2,4)
        self.img = pygame.image.load('imgs/cards/smaller_pngs/black_joker.png').convert_alpha()
        self.normal = self.img
        self.jumping = pygame.image.load('imgs/cards/final_jump/black_joker.png').convert_alpha()

        self.uid = uid
        self.rect.inflate_ip(100, 145)

    def draw(self):
        self.game.screen.blit(self.img,
                              self.rect.move(-self.game.player.viewx1, 0))

    def tick(self):
        w = self.thing_at(wall.Wall, self.vx, 0) or (
            self.thing_at(Shadow, self.vx, 0))
        if w:
            if w.rect.x > self.rect.x:
                self.rect.right = w.rect.left
            else:
                self.rect.left = w.rect.right
            self.vx = 0
        else:
            self.rect.x += self.vx

        w = self.thing_at(wall.Wall, 0, self.vy) or (
            self.thing_at(Shadow, 0, self.vy)) or (
            self.thing_at(Ship, 0, self.vy))
        if w:
            if self.vy > 0:
                self.rect.bottom = w.rect.top
                self.vy = 0
            else:
                self.rect.top = w.rect.bottom
                self.vy = 1
        else:
            self.rect.y += self.vy
            self.vy += 1
            if self.vy > 12:
                self.vy = 12

        if self.vy < 0:
            self.img = self.jumping
            fire.Fire(self.game, self.rect.centerx,
                                 self.rect.centery, -self.vx, -self.vy)
        else:
            self.img = self.normal

class Ship(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Ship, self).__init__(game)
        self.card_count = 0
        self.rect.move_ip(x, y)
        self.descriptor = descriptor
        self.img = pygame.image.load('imgs/cards/smaller_pngs/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.normal = self.img
        self.jumping = pygame.image.load('imgs/cards/final_jump/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.xstart = x
        self.ystart = y
        self.viewx1 = x-constants.WIDTH/2
        self.rect.inflate_ip(100, 145)
        self.keys = 0
        #self.img = pygame.image.load('imgs/cards/players/player.png').convert_alpha()
        #self.normal = self.img
        #self.jumping = pygame.image.load('imgs/cards/final_jump/jack_of_hearts2.png').convert_alpha()
        self.firing = False
        self.dead_ticks = 0

    def gotoDead(self):
        Death(self.game, self.img, self.rect.centerx, self.rect.centery)
        self.dead_ticks = constants.DEAD_TIME

    def tick(self):
        if self.dead_ticks > 0:
            self.dead_ticks -= 1
            self.rect.x = 300
            self.rect.y = 4444
            if self.dead_ticks == 0:
                self.rect.x = self.xstart
                self.rect.y = self.ystart
            return False

        self.fly()

        w = self.thing_at(wall.Wall, self.vx, 0) or (
            self.thing_at(Shadow, self.vx, 0))
        if w:
            if w.rect.x > self.rect.x:
                self.rect.right = w.rect.left
            else:
                self.rect.left = w.rect.right
            self.vx = 0
        else:
            self.rect.x += self.vx

        w = self.thing_at(wall.Wall, 0, self.vy) or (
            self.thing_at(Shadow, 0, self.vy))
        if w:
            if self.vy > 0:
                self.rect.bottom = w.rect.top
                self.vy = 0
                if ((self.keys & 4)>>2) > 0:
                    self.vy = -20
                    self.rect.y -= 1
            else:
                self.rect.top = w.rect.bottom
                self.vy = 1
        else:
            self.rect.y += self.vy
            self.vy += 1
            if self.vy > 12:
                self.vy = 12

        w = self.thing_at(spikes.Spike, 0, 1)
        if self.rect.y > constants.HEIGHT*1.5 or w:
            self.gotoDead()

        if not self.game.winning:
            self.viewx1 = self.rect.x-constants.WIDTH/2
        if self.vy < 0:
            self.img = self.jumping
            fire.Fire(self.game, self.rect.centerx,
                                 self.rect.centery, -self.vx, -self.vy)
        else:
            self.img = self.normal

    def draw(self):
        self.game.screen.blit(self.img, self.rect.move(-self.viewx1, 0))
        
    def handleKeyDown(self, k):
        if k == 'a':
            self.keys |= 1
        elif k == 'd':
            self.keys |= 2
        elif k == 'w':
            self.keys |= 4
        elif k == 's':
            self.keys |= 8

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
        self.vx = (((self.keys & 2)>>1) - ((self.keys & 1)>>0)) * 7

    def handleMDOWN(self, xxt, yyt):
        self.firing = True

    def handleMUP(self, xxt, yyt):
        self.firing = False
    
    def force_collect(self, descriptor):
        self.descriptor = descriptor
        self.img = pygame.image.load('imgs/cards/smaller_pngs/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.normal = self.img
        self.jumping = pygame.image.load('imgs/cards/final_jump/{}'.format(data.num_as_key[descriptor])).convert_alpha()


    def collect(self, descriptor):
        if int((str(descriptor)[3:])) > int((str(self.descriptor)[3:])):
            return
        else:
            self.card_count += 1
            self.force_collect(descriptor)

class Death(sprite.Sprite):
    def __init__(self, game, img, x, y):
        super(Death, self).__init__(game)
        self.img1 = img
        self.img2 = pygame.image.load('imgs/cards/backs/back.png').convert_alpha()
        self.rect.move_ip(x - self.game.player.viewx1, y)
        self.rect.inflate_ip(100, 145)
        self.imgs  = img
        self.state = 0
        self.width = 100
        self.timer = 10

    def tick(self):
        self.img = pygame.transform.scale(self.imgs, (self.width, 145))
        if self.state == 0: #frozen
            self.timer -= 1
            if self.timer < 0:
                self.timer = 10
                self.state = 1
        elif self.state == 1: #shrinking
            if self.width > 1:  #we have room to shrink
                self.width -= 7
                if self.width < 0: self.width = 0
            else:
                self.imgs = self.img2 #do the flip
                self.state = 2
        elif self.state == 2: #growing
            self.width += 7
            if self.width >= 100:
                self.state = 3
        elif self.state == 3: #frozen again
            self.timer -= 1
            if self.timer < 0:
                self.state = 4
        elif self.state == 4: #fall
            self.rect.move_ip(0, self.vy)
            self.vy -= 1
            if self.rect.y < -100:
                return True #die

    def draw(self):
        #draw our sprite to the screen
        self.game.screen.blit(self.img, self.rect.move((100-self.width)/2, 0))
