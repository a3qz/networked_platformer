import random
import pygame
import time
import sys
import math
import fire
import sprite
import constants
import wall
import spikes
import data
import player

# spades = 1 hearts = 2 diamonds = 3 clubs = 4
class Collectable(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Collectable, self).__init__(game)
        self.descriptor = descriptor
        self.rect.move_ip(x, y)
        self.xstart = x
        self.ystart = y
        self.viewx1 = x-constants.WIDTH/2
        self.rect.inflate_ip(100, 145)
        self.keys = 0
        self.img = pygame.image.load('imgs/cards/smaller_pngs/' + data.num_as_key[str(descriptor)]).convert_alpha()
        self.normal = self.img
        self.firing = False
        self.dead_ticks = 0

    def collectable_check(self, new_desc):
        #ok, so, we delimit suit and rank by... a 9...
        ugh = str(self.descriptor)
        #but it's always of the form 9S9R or 9S9RR
        #where S is suit [1-4] and R/RR is rank [1-13]
        # in this one we also check if opposite suit
        #so, calculate our new stuff
        newsuit = ugh[1]
        if ugh[-2] == '9':
            newrank = ugh[-1]
        else:
            newrank = ugh[-2:]
        #then do the thing
        newrank = str(int(newrank)+1) #why ryan why
        #then do the thing
        newcollect = '9' + newsuit + '9' + newrank
        if (new_desc[1] == '1' or new_desc[1] == '4'):
            suitlooking = 'r'
        else:
            suitlooking = 'b'

        if (suitlooking == 'b' and (newcollect[1] == '1' or newcollect[1] == '4')) or (suitlooking == 'r' and (newcollect[1] == '2' or newcollect[1] == '3')):
            print 'ere'
            return new_desc[2:] == newcollect[2:]
        return False
            





    def gotoDead(self):
        #ok, so, we delimit suit and rank by... a 9...
        ugh = str(self.descriptor)
        #but it's always of the form 9S9R or 9S9RR
        #where S is suit [1-4] and R/RR is rank [1-13]
        #so, calculate our new stuff
        newsuit = ugh[1]
        if ugh[-2] == '9':
            newrank = ugh[-1]
        else:
            newrank = ugh[-2:]
        #then do the thing
        newrank = str(int(newrank)-1) #why ryan why
        #then do the thing
        newcollect = '9' + newsuit + '9' + newrank
        #then update the player sprite
        self.game.player.collect(newcollect)
        #and kill ourselves
        self.dead_ticks = constants.DEAD_TIME

    def tick(self):
        if self.dead_ticks > 0:
            #self.dead_ticks -= 1
            self.rect.x = 300
            self.rect.y = 4444
            #if self.dead_ticks == 0:
                #self.rect.x = self.xstart
                #self.rect.y = self.ystart
            return False
        w = (
            self.thing_at(player.Shadow, 0, 0)) or (
            self.thing_at(player.Ship, 0, 0))

        if w:
            if self.collectable_check(self.game.player.descriptor):
                self.gotoDead()
            else:
                print '\a'
                print 'cant collect'
                #eventually put bad animation here

    def draw(self):
        self.game.screen.blit(self.img, self.rect.move(-self.game.player.viewx1, 0))
        
