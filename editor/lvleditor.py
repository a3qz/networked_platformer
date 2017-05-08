#!/usr/bin/python2 -B
import sys
sys.path.insert(0,'.')

import os
import pygame
import math
import editor
import constants

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(constants.SIZE)
game = editor.Game(screen)


def go():
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
        game.tick()
        game.draw()
        pygame.display.flip()
        clock.tick(constants.FPS)
    except Exception as E:
        print "here " + str(E)

def exit():
    game.board.save("./levels/beta.lvl")
    os._exit(0)

while True:
    go()
