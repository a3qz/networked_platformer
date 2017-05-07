import random
import time
import sys
import player
import constants
import client
from struct import *
import board

class Game:
    def __init__(self, s):
        self.objects = []
        self.screen = s
        self.player = player.Ship(self, 100, 100, "93913")
        self.connection = None
        self.level = 1
        self.t = 0
        client.DaFactory(self)
        self.board = board.Board(self)
        self.board.parse("./levels/1.lvl")


    def tick(self):
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
        for b in reversed(self.objects):
            b.draw()

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
 
    def handleData(self, data):
        uid = unpack("B", data[0])[0]
        data = unpack("BiiiiB", data[1:22])
        if data[0] == 0: #player update
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
            print data
            if self.level != data[2]:
                self.level = data[2] #level number
                self.board.parse("./levels/{}.lvl".format(self.level))
        elif data[0] == 2: #kill a card
            for o in self.game.objects:
                if isinstance(o, collectable.Collectable) and o.descriptor == data[1]:
                    o.gotoDead()


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
