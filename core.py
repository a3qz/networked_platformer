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

class Game:
    def __init__(self, s):
        self.objects = []
        self.screen = s
        self.player = player.Ship(self, 100, 100)
        self.connection = None
        self.t = 0
        client.DaFactory(self)
        for i in range(0, constants.WIDTH, 32):
            wall.Wall(self, i, constants.HEIGHT-32)


    def tick(self):
        try:
            for b in self.objects:
                if b.tick():
                   b.die()
                   self.objects.remove(b)
            self.t = (self.t + 1) % 2
            if self.t == 0:
                self.sendPlayer()
        except Exception as E:
            print E

    def draw(self):
        for b in reversed(self.objects):
            b.draw()

    def handleKeyDown(self, k):
        self.player.handleKeyDown(k)
    def handleKeyUp(self, k):
        self.player.handleKeyUp(k)
    def handleMUP(self, xxt, yyt):
        self.player.handleMUP(xxt, yyt)
    def handleMDOWN(self, xxt, yyt):
        self.player.handleMDOWN(xxt, yyt)
 
    def handleData(self, data):
        uid = unpack("B", data[0])[0]
        data = unpack("BIIiiB", data[1:22])
        #data is in the form (SENDER_ID, MESSAGE_TYPE, data...)
        if data[0] == 0:
            #then data is a join message
            player.Shadow(self, uid)
            print "PLAYER {} JOINED!".format(uid)
        elif data[0] == 1:
            #then data is an update message
            for o in self.objects:
                if isinstance(o, player.Shadow) and o.uid == uid:
                    o.x  = data[1]
                    o.y  = data[2]
                    o.vx = data[3]
                    o.vy = data[4]

    def sendPlayer(self):
        if not self.connection: return
        self.connection.send(pack("BIIiiB", 1, self.player.x,
                                               self.player.y,
                                               self.player.vx,
                                               self.player.vy,
                                               0))

    def connected(self, connection):
        self.connection = connection
        self.connection.send(pack("BIIiiB", 0, 0, 0, 0, 0, 0))
