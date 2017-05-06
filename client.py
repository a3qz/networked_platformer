#!/usr/bin/python2
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
#from twisted.internet.task import LoopingCall
from twisted.internet.defer import DeferredQueue

HOME_HOST = "localhost"
HOME_PORT = 40060

class DaBears(Protocol):
    def __init__(self, game):
        self.game = game
        self.q = DeferredQueue()

    def connectionMade(self):
        self.startForwarding() 
        self.game.connected(self)

    def startForwarding(self):
        self.q.get().addCallback(self.wordForward)

    def wordForward(self, data):
        self.transport.write(data)
        self.q.get().addCallback(self.wordForward)

    def dataReceived(self, data):
        self.game.handleData(data)

    def send(self, data):
        self.transport.write(data)
        #self.q.put(data)

class DaFactory(ClientFactory):
    def __init__(self, game):
        self.myconn = DaBears(game)
        reactor.connectTCP(HOME_HOST, HOME_PORT, self)

    def buildProtocol(self, addr):
        return self.myconn
