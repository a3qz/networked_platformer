#!/usr/bin/python2
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from struct import *
import sys, getopt
import constants

CLIN_PORT = 40060

MODE = constants.VERSUS

if len(sys.argv) > 2:
    print "Incorrect number of arguments"
    sys.exit(1)
elif len(sys.argv) == 2:
    if sys.argv[1] == "-c":
        MODE = constants.COOPERATIVE
    elif sys.argv[1] == "-v":
        MODE = constants.VERSUS
    else:
        print "Invalid flag.  Usage: ./server.py -[cv]"
        print "    -v    versus mode"
        print "    -c    cooperative mode"
        print "default is versus mode"
        sys.exit(1)

class ClientConnection(Protocol):
    def __init__(self, factory, uid):
        self.factory = factory
        self.uid = uid
        pass

    def connectionMade(self):
        print("Client connected!")
        self.factory.addMore()
        self.q = DeferredQueue()

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
        parsed = unpack("BiiiiB", data[0:21])
        if parsed[0] == 1:
            data = pack("BiiiiB", 1, MODE, self.factory.level, 0, 0, 0)
            #if a client asked for something,
            #just give it to them
            self.transport.write(pack("B", self.uid) + data)
        else: #otherwise forward it
            self.factory.send(self, data)

class ClientConnectionFactory(ClientFactory):
    def __init__(self):
        self.cards = []
        self.level = 2
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
