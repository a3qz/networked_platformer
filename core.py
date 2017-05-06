import random
import time
import sys
import player
import enemy
import bullet
import fire
import wall
import constants
import client
from struct import *
import board

class Game:
    def __init__(self, s):
        self.objects = []
        self.screen = s
        self.player = player.Ship(self, 100, 100)
        self.connection = None
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
        data = unpack("BIIiiB", data[1:22])
        for o in self.objects:
            if isinstance(o, player.Shadow) and o.uid == uid:
                o.x  = data[1]
                o.y  = data[2]
                o.vx = data[3]
                o.vy = data[4]
                return
        o = player.Shadow(self, uid)
        o.x  = data[1]
        o.y  = data[2]
        o.vx = data[3]
        o.vy = data[4]
        print "PLAYER {} JOINED!".format(uid)

    def sendPlayer(self):
        if not self.connection: return
        self.connection.send(pack("BIIiiB", 1, self.player.x,
                                               self.player.y,
                                               self.player.vx,
                                               self.player.vy,
                                               0))

    def connected(self, connection):
        self.connection = connection
