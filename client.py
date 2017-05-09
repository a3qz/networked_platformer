#!/usr/bin/python2

#our client networking stuff is in here - it just handles recieving
#information - all of the stuff is really handled in core

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

HOME_HOST = "newt.campus.nd.edu"
HOME_PORT = 40060

class DaBears(Protocol):
    def __init__(self, game):
        #set our game state when we are initialized
        self.game = game

    def connectionMade(self):
        #when we are connected, tell our game state about it
        self.game.connected(self)

    def dataReceived(self, data):
        #have our game state handle any recieved data
        self.game.handleData(data)

    def send(self, data):
        #simply send data
        self.transport.write(data)

class DaFactory(ClientFactory):
    def __init__(self, game):
        #make a connection to the server
        self.myconn = DaBears(game)
        reactor.connectTCP(HOME_HOST, HOME_PORT, self)

    def buildProtocol(self, addr):
        return self.myconn

#note that the core game object will do the reactor goodness
