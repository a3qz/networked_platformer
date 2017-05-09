import random
import pygame
import time
import sys
import math
import data
import sprite
import constants
import wall
import spikes

# this contains the classes for our players and our "other player" - shadow is the network player, ship is the one the player controls

# network player class
class Shadow(sprite.Sprite):
    def __init__(self, game, uid):
        super(Shadow, self).__init__(game)
        self.num = random.randint(2,4)
        # all computer players appear as jokers
        self.img = pygame.image.load('imgs/cards/smaller_pngs/black_joker.png').convert_alpha()
        self.normal = self.img
        self.jumping = pygame.image.load('imgs/cards/final_jump/black_joker.png').convert_alpha()

        self.uid = uid
        self.rect.inflate_ip(100, 145)

    # blit your image to the screen offset by the player's view window
    def draw(self):
        self.game.screen.blit(self.img,
                              self.rect.move(*self.game.player.view))

    # do the movement, mostly checking for collisions
    def tick(self):
        # make sure that the shadow does not run through a wall
        w = self.thing_at(wall.Wall, self.vx, 0) or (
            self.thing_at(Shadow, self.vx, 0))
        # if colliding with wall stop it
        if w:
            if w.rect.x > self.rect.x:
                self.rect.right = w.rect.left
            else:
                self.rect.left = w.rect.right
            self.vx = 0
        else:
            self.rect.x += self.vx

        # make sure it does not fall through a wall
        w = self.thing_at(wall.Wall, 0, self.vy) or (
            self.thing_at(Shadow, 0, self.vy)) or (
            self.thing_at(Ship, 0, self.vy))
        # if on a wall stop it
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
        else:
            self.img = self.normal


# this is the class for the player
class Ship(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Ship, self).__init__(game)
        self.card_count = 0
        self.rect.move_ip(x, y)
        self.descriptor = descriptor
        # load in the image of the descriptor
        self.img = pygame.image.load('imgs/cards/smaller_pngs/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.normal = self.img
        self.jumping = pygame.image.load('imgs/cards/final_jump/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.xstart = x
        self.ystart = y
        self.view = (0, 0)
        self.rect.inflate_ip(100, 145)
        self.keys = 0
        self.firing = False
        self.dead_ticks = 0

    #kill self for a small amount of time
    def gotoDead(self):
        Death(self.game, self.img, self.rect.centerx, self.rect.centery)
        self.dead_ticks = constants.DEAD_TIME

    # increment self
    def tick(self):
        # if dead, increment 
        if self.dead_ticks > 0:
            self.dead_ticks -= 1
            self.rect.x = 300
            self.rect.y = 4444
            # if should not be dead, bring back to life
            if self.dead_ticks == 0:
                self.rect.x = self.xstart
                self.rect.y = self.ystart
            return False

        #handle horizontal motion buttons
        self.fly()

        #check if we're about to move into a wall or player
        w = self.thing_at(wall.Wall, self.vx, 0) or (
            self.thing_at(Shadow, self.vx, 0))
        if w: #if so, move us into them and stop
            if w.rect.x > self.rect.x:
                self.rect.right = w.rect.left
            else:
                self.rect.left = w.rect.right
            self.vx = 0
        else: #if not, do the horizontal movement
            self.rect.x += self.vx

        #check if we're about to move vertically into a wall or player
        w = self.thing_at(wall.Wall, 0, self.vy) or (
            self.thing_at(Shadow, 0, self.vy))
        if w: #if so, move into it
            if self.vy > 0:
                #if we're falling, align with its top and stop falling
                self.rect.bottom = w.rect.top
                #if we're in the win state, we bounce!
                if self.game.winning:
                    #stop bouncing after a while
                    if self.vy <= 5:
                        self.vy = 0
                    else: #bounce!
                        self.vy = -(self.vy*5)/8
                else:
                    #otherwise, when we hit the ground we stop
                    self.vy = 0
                #while on the ground we can jump, so handle that
                if ((self.keys & 4)>>2) > 0:
                    self.vy = -20
                    self.rect.y -= 1
            else:
                #if we move upward into something, stop and fall back down
                self.rect.top = w.rect.bottom
                self.vy = 1
        else:
            #if we won't hit anything, move vertically
            self.rect.y += self.vy
            #and let gravity do its thing
            self.vy += 1
            #but don't go tooo fast
            if self.vy > 16:
                self.vy = 16

        #check if we're coliding with spikes
        w = self.thing_at(spikes.Spike, 0, 1)
        if self.rect.y > self.game.deathzone or w:
            self.gotoDead()

        #move our viewport if we aren't in the win state
        if not self.game.winning:
            self.view = (constants.WIDTH/2 - self.rect.x - self.rect.w/2,
                         (constants.HEIGHT*5)/8 - self.rect.y - self.rect.h/2)

        #set our sprite to either the jumping one or the normal one
        if self.vy < 0:
            self.img = self.jumping
        else:
            self.img = self.normal

    def draw(self):
        #draw ourselves
        self.game.screen.blit(self.img, self.rect.move(*self.view))
        

    def handleKeyDown(self, k):
        #set our key variable based off what we're pressing
        if k == 'a':
            self.keys |= 1
        elif k == 'd':
            self.keys |= 2
        elif k == 'w':
            self.keys |= 4
        elif k == 's':
            self.keys |= 8

    def handleKeyUp(self, k):
        #set our key variable based off what we're releasing
        if k == 'a':
            self.keys &= ~1
        elif k == 'd':
            self.keys &= ~2
        elif k == 'w':
            self.keys &= ~4
        elif k == 's':
            self.keys &= ~8

    # handle walking (it was called fly because of the deathstar thing
    # and we didn't rename it)
    def fly(self):
        self.vx = (((self.keys & 2)>>1) - ((self.keys & 1)>>0)) * 7

    def handleMDOWN(self, xxt, yyt):
        self.firing = True

    def handleMUP(self, xxt, yyt):
        self.firing = False
    
    # force it to change to whatever we want (used for reset) 
    def force_collect(self, descriptor):
        self.descriptor = descriptor
        self.img = pygame.image.load('imgs/cards/smaller_pngs/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        self.normal = self.img
        self.jumping = pygame.image.load('imgs/cards/final_jump/{}'.format(data.num_as_key[descriptor])).convert_alpha()


    # check if a card is collectable and load it
    def collect(self, descriptor):
        if int((str(descriptor)[3:])) > int((str(self.descriptor)[3:])):
            return
        else:
            self.force_collect(descriptor)

# sprite for death animation
class Death(sprite.Sprite):
    def __init__(self, game, img, x, y):
        super(Death, self).__init__(game)
        self.img1 = img
        self.img2 = pygame.image.load('imgs/cards/backs/back.png').convert_alpha()
        self.rect.move_ip(x, y)
        self.rect.move_ip(*self.game.player.view)
        self.rect.inflate_ip(100, 145)
        self.imgs  = img
        self.state = 0
        self.width = 100
        self.timer = 10

    # amimate ourself for the flip
    def tick(self):
        self.img = pygame.transform.scale(self.imgs, (self.width, 145))
        # check state and adjust timer
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
