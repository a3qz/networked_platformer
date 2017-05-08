import random
import pygame
import time
import sys
import player
import constants
import collectable
import client
from struct import *
import board

class Game:
    def __init__(self, s):
        self.objects = []
        self.losing = 2
        self.screen = s
        self.player = player.Ship(self, 100, 100, "91913")
        self.connection = None
        self.deathzone = 5000
        self.level = 1
        self.t = 0
        self.mode = 0
        client.DaFactory(self)
        self.board = board.Board(self)
        self.board.parse("./levels/3.lvl")
        self.winning = False
        self.font = pygame.font.Font("./fonts/megaman_2.ttf", 16)
        self.bigfont = pygame.font.Font("./fonts/megaman_2.ttf", 32)


    def tick(self):
        self.did_game_end()
        try:
            for b in self.objects:
                if b.tick():
                   b.die()
                   self.objects.remove(b)
            self.t = (self.t + 1) % 20
            if self.t == 0:
                self.sendPlayer()
        except Exception as E:
            print E

    def draw(self):
        if not self.connection:
            self.screen.fill(constants.GRAY)
            label = self.bigfont.render("JOINING GAME", 1, (255, 255, 255))
            self.screen.blit(label, (constants.WIDTH/2-170, 300))
            return

        if not self.winning or not self.losing == 2:
            self.screen.fill(constants.GREEN)
        for b in reversed(self.objects):
            b.draw()
        if self.mode == constants.VERSUS:
            label = self.font.render("SCORE: "+str(self.player.card_count), 1, (255, 255, 255))
            self.screen.blit(label, (25, 25))
        if self.losing == 1:
            self.screen.fill(constants.RED)
            label = self.bigfont.render("You Lose", 1, (255, 255, 255))
            self.screen.blit(label, (constants.WIDTH/2-125, 300))
        if self.winning and not self.losing == 1:
            label = self.bigfont.render("You Win!!", 1, (255, 255, 255))
            self.screen.blit(label, (constants.WIDTH/2-125, 200))


    def handleKeyDown(self, k):
        self.player.handleKeyDown(k)
        self.sendPlayer()
    def handleKeyUp(self, k):
        self.player.handleKeyUp(k)
        self.sendPlayer()
    def handleMUP(self, xxt, yyt):
        self.player.handleMUP(xxt, yyt)
    def handleMDOWN(self, xxt, yyt):
        self.player.handleMDOWN(xxt, yyt)
 
    def handleData(self, d):
        for x in range(0, len(d), 22):
            data = d[x:x+22]
            if len(data) != 22:
                print "dropping packet: " + repr(data)
                return
            uid = unpack("B", data[0])[0]
            data = unpack("BiiiiB", data[1:22])
            if data[0] == 0: #player update
                if uid == 0: #server message
                    continue #invalid message
                for o in self.objects:
                    if isinstance(o, player.Shadow) and o.uid == uid:
                        o.rect.x  = data[1]
                        o.rect.y  = data[2]
                        o.vx = data[3]
                        o.vy = data[4]
                        return
                o = player.Shadow(self, uid)
                o.rect.x  = data[1]
                o.rect.y  = data[2]
                o.vx = data[3]
                o.vy = data[4]
                print "PLAYER {} JOINED!".format(uid)
            elif data[0] == 1: #gametype
                self.mode = data[1] #VERSUS or COOPERATIVE
                self.winning = False
                self.player.force_collect("91913")
                self.player.rect.x = self.player.xstart
                self.player.rect.y = self.player.ystart
                self.player.card_count = 0
                self.losing = 2
                print data
                self.level = data[2] #level number
                self.board.parse("./levels/{}.lvl".format(self.level))
            elif data[0] == 2: #kill a card
                for o in self.objects:
                    if isinstance(o, collectable.Collectable) and o.descriptor == data[1]:
                        o.gotoDead()
            elif data[0] == 3:
                if self.mode == constants.VERSUS:
                    if data[1] > self.player.card_count:
                        self.winning = False
                        self.losing = 1


    def sendPlayer(self):
        if not self.connection: return
        self.connection.send(pack("BiiiiB", 0, self.player.rect.x,
                                               self.player.rect.y,
                                               self.player.vx,
                                               self.player.vy,
                                               0))

    def connected(self, connection):
        self.connection = connection
        self.connection.send(pack("BiiiiB", 1, 0, 0, 0, 0, 0))

    def did_game_end(self):
        if str(self.player.descriptor)[3:] == "1":
            self.handle_win()

    def collectCard(self, n):
        self.connection.send(pack("BiiiiB", 2, n, 0, 0, 0, 0))

    def handle_win(self):
        if not self.winning:
            self.connection.send(pack("BiiiiB", 3, self.player.card_count, 0, 0, 0, 0))
        self.winning = True

