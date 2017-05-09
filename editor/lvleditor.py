#!/usr/bin/python2 -B
#we need the modules from the current working directory, which is our
#parent directory, but you run us from there
import sys
sys.path.insert(0,'.')

import os
import pygame
import math
import editor
import constants

#start pygame, set the size, make a game state, and start a clock
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(constants.SIZE)
game = editor.Game(screen)


def go():
    #handle events
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP: #handle clicking
                mx, my = event.pos
                game.handleMUP(mx, my)
            elif event.type == pygame.MOUSEBUTTONDOWN: #handle clicking
                mx, my = event.pos
                game.handleMDOWN(mx, my, event)
            elif event.type == pygame.KEYUP:          #handle key releases
                k = pygame.key.name(event.key)
                game.handleKeyUp(k)
            elif event.type == pygame.KEYDOWN:        #handle key presses
                k = pygame.key.name(event.key)
                game.handleKeyDown(k)
                if "q" in k:
                    exit()
        #tick the game
        game.tick()
        #draw the game
        game.draw()
        #flip the framebuffer
        pygame.display.flip()
        #handle the timing
        clock.tick(constants.FPS)
    except Exception as E:
        print "here " + str(E)

def exit():
    #save the created level before closing
    game.board.save("./levels/beta.lvl")
    #close, hard!
    os._exit(0)

while True:
    go()
