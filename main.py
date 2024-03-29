#!/usr/bin/python2 -B
import os
import pygame
import math
import core
import constants
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

# this program is our main executable
# initilize the things we need (pygame, the game loop, our screen, the clock)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(constants.SIZE)
game = core.Game(screen)

# main game loop
def go():
    try:
        # handle the pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                print("lol")
                os._exit(0) #handle quitting
            elif event.type == pygame.MOUSEBUTTONUP: #handle clicking
                mx, my = event.pos
                game.handleMUP(mx, my)
            elif event.type == pygame.MOUSEBUTTONDOWN: #handle clicking
                mx, my = event.pos
                game.handleMDOWN(mx, my)
            elif event.type == pygame.KEYUP:          #handle key releases
                k = pygame.key.name(event.key)
                game.handleKeyUp(k)
            elif event.type == pygame.KEYDOWN:        #handle key presses
                k = pygame.key.name(event.key)
                game.handleKeyDown(k)
                if "q" in k:
                    print("q")
                    os._exit(0)
        # call tick function on game which calls it on every object
        game.tick()
        # call the draw function which calls every object
        game.draw()
        pygame.display.flip()
        clock.tick(constants.FPS)
    except Exception as E:
        pass
print("kk")
# call go in a loop for the main execution
lc = LoopingCall(go)
lc.start(0.001)
reactor.run()
print("henlo?")
