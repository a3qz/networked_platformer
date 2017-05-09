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
        self.objects = [] #start with a list of no objects
        self.screen = s   #get the screen surface
        #make a player ship to use to control the view
        self.player = Ship(self, 100, 100, "91913")
        #load a font for drawing our typed string
        self.bigfont = pygame.font.Font("./fonts/megaman_2.ttf", 32)
        #make a board and load in the level editor level
        self.board = board.Board(self)
        self.board.parse("./levels/beta.lvl")

    def tick(self): #handle just our player for the editor
        self.player.tick()

    def draw(self):
        #draw the background
        self.screen.fill(constants.GREEN)
        #draw the objects in reversed order, for depth reasons
        for b in reversed(self.objects):
            b.draw()

    #handle player actions
    def handleKeyDown(self, k):
        self.player.handleKeyDown(k)
    def handleKeyUp(self, k):
        self.player.handleKeyUp(k)

    #no longer used
    def handleMUP(self, xxt, yyt):
        pass

    def handleMDOWN(self, xxt, yyt, event):
        #figure out which grid space the player clicked on
        x = int((16 + xxt - self.player.view[0])/32)*32
        y = int((16 + yyt - self.player.view[1])/32)*32
        #check if they are left clicking or not
        if event.button == 1:
            #if left click, add a thing to the board based off
            #where you clicked and what the user typed
            self.board.ref[int(self.player.toadd)](self, x, y,
                    int(self.player.toadd))
        else:
            #otherwise, make a rectangle and figure out who you clicked on
            rect = pygame.Rect(0, 0, 1, 1)
            l1 = self.objects
            l2 = [w.rect for w in l1]
            #check the objects for collision
            i = rect.move(x, y).collidelist(l2)
            #if we clicked on a valid thing to remove, remove it
            if i != -1 and not isinstance(l1[i], Ship):
                self.objects = [o for o in self.objects if o != l1[i]]  
 
class Ship(sprite.Sprite):
    def __init__(self, game, x, y, descriptor):
        super(Ship, self).__init__(game)
        self.rect.move_ip(x, y) #move to the correct coordinates
        #load an image
        self.img = pygame.image.load('imgs/cards/smaller_pngs/{}'.format(data.num_as_key[descriptor])).convert_alpha()
        #set up our game's viewport
        self.view = (0, 0)
        #start a string for typing
        self.toadd = ''
        #make us our correct size
        self.rect.inflate_ip(100, 145)
        #we aren't pressing anything
        self.keys = 0

    def tick(self):
        #move us based off our velocity
        self.rect.move_ip(self.vx, self.vy)
        #move our view to the right place
        self.view = (constants.WIDTH/2 - self.rect.x,
                     (constants.HEIGHT*3)/4 - self.rect.y)
        #handle keys
        self.fly()

    def draw(self):
        self.game.screen.blit(self.img, self.rect.move(*self.view))
        label = self.game.bigfont.render(self.toadd, 1, (255, 255, 255))
        self.game.screen.blit(label, (10, 10))
        
    def handleKeyDown(self, k):
        #asdw control flight
        if k == 'a':
            self.keys |= 1
        elif k == 'd':
            self.keys |= 2
        elif k == 'w':
            self.keys |= 4
        elif k == 's':
            self.keys |= 8
        elif k.isdigit() and len(k) == 1: #if we did a single digit, type it
            self.toadd = self.toadd + k
        elif k == 'backspace': #if we backspaced, delete a char from our string
            self.toadd = self.toadd[:-1]

    #stop flying when releasing keys
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
        #handle our velocities
        self.vx = (((self.keys & 2)>>1) - ((self.keys & 1)>>0)) *  7
        self.vy = (((self.keys & 4)>>2) - ((self.keys & 8)>>3)) * -7
