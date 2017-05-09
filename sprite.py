import random
import pygame
import time
import sys
import math

# class that all of our objects inherit from 
class Sprite(object):
    def __init__(self, game):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.vx = 0
        self.vy = 0
        self.game = game
        # put self in the game objects list so it calls the draw and tick of them
        game.objects.append(self)

    # adjust the movement based on velocity
    def tick(self):
        self.rect.move_ip(self.vx, self.vy)
        
    # overload this
    def draw(self):
        pass

    # overload this
    def die(self):
        pass

    # tell the what we collide with if we make a movement 
    def thing_at(self, c, x, y):
        l1 = [w for w in self.game.objects
                if isinstance(w, c) and self != w]
        l2 = [w.rect for w in l1]
        i = self.rect.move(x, y).collidelist(l2)
        if i == -1:
            return None
        else:
            return l1[i]
