#!/usr/bin/python2
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from struct import *

CLIN_PORT = 40060

class ClientConnection(Protocol):
    def __init__(self, factory, uid):
        self.factory = factory
        self.uid = uid
        pass

    def connectionMade(self):
        print("Client connected!")
        self.factory.addMore()
        self.q = DeferredQueue()
        #self.startForwarding()
        self.factory.sendMe(self, pack("BIIiiB", 0, 0, 0, 0, 0, 0))

    def startForwarding(self):
        self.q.get().addCallback(self.wordForward)

    def wordForward(self, data):
        try:
            self.factory.send(self, data)
            self.q.get().addCallback(self.wordForward)
        except Exception as E:
            print E

    def dataReceived(self, data):
        #self.transport.write(data)
        #self.q.put(data)
        self.factory.send(self, data)

class ClientConnectionFactory(ClientFactory):
    def __init__(self):
        self.count = 0
        self.cons = []
        self.addMore()

    def buildProtocol(self, addr):
        return self.cons[-1]

    def addMore(self):
        self.cons.append(ClientConnection(self, self.count))
        self.count += 1

    def sendMe(self, guy, data):
        for c in self.cons:
            if c.uid != guy.uid:
                guy.transport.write(pack("B", c.uid) + data)

    def send(self, guy, data):
        for c in self.cons:
            if c.uid != guy.uid and c.transport:
                c.transport.write(pack("B", guy.uid) + data)
        
reactor.listenTCP(CLIN_PORT, ClientConnectionFactory())
reactor.run()
