#!/usr/bin/python2 -B
import sys
import pygame
import math
import core
import constants
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(constants.SIZE)
game = core.Game(screen)

def go():
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit() #handle quitting
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
                    sys.exit()
        screen.fill(constants.GREEN)
        game.tick()
        game.draw()
        pygame.display.flip()
        clock.tick(constants.FPS)
    except Exception as E:
        print E
lc = LoopingCall(go)
lc.start(0.001)
reactor.run()
