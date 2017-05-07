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

    def gotoDead(self):
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
            self.gotoDead()

    def draw(self):
        self.game.screen.blit(self.img, self.rect.move(-self.game.player.viewx1, 0))
        
