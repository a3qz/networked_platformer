import random
import pygame
import time
import sys
import math
import sprite
import constants
import wall
import spikes
import data
import player

# spades = 1 hearts = 2 diamonds = 3 clubs = 4

# these are the cards that you collect
class Collectable(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Collectable, self).__init__(game)
        self.invalid_collect = 0
        self.descriptor = descriptor
        self.rect.move_ip(x, y)
        self.xstart = x
        self.ystart = y
        self.viewx1 = x-constants.WIDTH/2
        self.rect.inflate_ip(100, 145)
        self.keys = 0
        self.img = pygame.image.load('imgs/cards/smaller_pngs/' + data.num_as_key[str(descriptor)]).convert_alpha() # loads in default cards
        self.normal = self.img
        self.firing = False
        self.dead_ticks = 0

    # check if you should be allowed to collect the object
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
        # increment the rank by 1 to make sure the thing touching us matches the thing that is allowed to pick us up
        newrank = str(int(newrank)+1) #why ryan why
        #then do the thing
        newcollect = '9' + newsuit + '9' + newrank

        # make sure that the suit is a different color then your own
        if (new_desc[1] == '1' or new_desc[1] == '4'):
            suitlooking = 'r'
        else:
            suitlooking = 'b'

        if (suitlooking == 'b' and (newcollect[1] == '1' or newcollect[1] == '4')) or (suitlooking == 'r' and (newcollect[1] == '2' or newcollect[1] == '3')):
            # check if your rank is the incremented one
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
        # decrement rank by one so we can gie the player the right one
        newrank = str(int(newrank)-1) #why ryan why
        #then do the thing
        newcollect = '9' + newsuit + '9' + newrank
        #then update the player sprite

        # call the player to collect us 
        self.game.player.collect(str(self.descriptor))
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

        #checks for a collision
        w = (self.thing_at(player.Ship, 0, 0))
            #self.thing_at(player.Shadow, 0, 0)) or (

        # check if we should be displaying the card with a red tint for cannot pickup
        if self.invalid_collect > 1:
            self.invalid_collect -= 1
        elif self.invalid_collect == 1:
            self.invalid_collect = 0
            self.img = self.normal

        # if there is a collision
        if w:
            # check if it is collectable
            if self.collectable_check(self.game.player.descriptor):
                self.game.player.card_count += 1
                self.game.collectCard(int(self.descriptor))
                self.gotoDead()
            # if it is not collectable, color it in a little
            else:
                # we are re-using this code from john's previous pygame project
                self.invalid_collect = constants.INVALID_COLLECT_TIMER
                n = pygame.Surface((100, 145), pygame.SRCALPHA, 32)
                m = self.img.copy()
                n.fill((127, 100, 100, 127))
                n.set_alpha(127)
                
                m.blit(n, (0,0), special_flags=pygame.BLEND_RGB_MIN)
                self.img = m
                self.game.screen.blit(m, self.rect.move(*self.game.player.view), special_flags=pygame.BLEND_ADD)

    # blit the image to the screen
    def draw(self):
        self.game.screen.blit(self.img, self.rect.move(*self.game.player.view))
        
