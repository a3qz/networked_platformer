#!/usr/bin/python2
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from threading import Timer
from struct import *
import sys, getopt
import constants

# set port number
CLIN_PORT = 40060

# default mode and port 
MODE = constants.VERSUS
LEVEL = 3

# parse command line arguments
if len(sys.argv) > 3:
    print "Incorrect number of arguments"
    sys.exit(1)
# if length is two
elif len(sys.argv) == 2:
    # if cooperative flag
    if sys.argv[1] == "-c":
        MODE = constants.COOPERATIVE
    # if versus flag
    elif sys.argv[1] == "-v":
        MODE = constants.VERSUS
    else:
        print "Invalid flag.  Usage: ./server.py -[cv]"
        print "    -v    versus mode"
        print "    -c    cooperative mode"
        print "    -l #  select level number #"
        print "default is versus mode"
        sys.exit(1)
# if length of 3 (need to fix this)
elif len(sys.argv) == 3:
    if sys.argv[1] == "-l":
        if int(sys.argv[2]) <= constants.NUM_LEVELS:
            LEVEL = sys.argv[2]
        else:
            print "invalid level number"
    else:
        print "Invalid flag.  Usage: ./server.py -[cv]"
        print "    -v    versus mode"
        print "    -c    cooperative mode"
        print "    -l #  select level number #"
        print "default is versus mode"
        sys.exit(1)
elif len(sys.argv) == 4:
    if sys.argv[1] == "-l":
        if int(sys.argv[2]) <= constants.NUM_LEVELS:
            LEVEL = sys.argv[2]
        else:
            print "invalid level number"
    elif sys.argv[1] == "-c":
        MODE = constants.COOPERATIVE
        if sys.argv[2] == "-l":
            if int(sys.argv[3]) <= constants.NUM_LEVELS:
                LEVEL = sys.argv[3]
            else:
                print "invalid level number"
    # if versus flag
    elif sys.argv[1] == "-v":
        MODE = constants.VERSUS
        if sys.argv[2] == "-l":
            if int(sys.argv[3]) <= constants.NUM_LEVELS:
                LEVEL = sys.argv[3]
            else:
                print "invalid level number"
    else:
        print "Invalid flag.  Usage: ./server.py -[cv] [-l #]"
        print "    -v    versus mode"
        print "    -c    cooperative mode"
        print "    -l #  select level number #"
        print "default is versus mode"
        sys.exit(1)



# client connection
class ClientConnection(Protocol):
    def __init__(self, factory, uid):
        self.factory = factory
        self.uid = uid
        pass

    # if connection is made
    def connectionMade(self):
        print("Client connected!")
        self.factory.addMore()
        self.q = DeferredQueue()

    # put callback onto queue
    def startForwarding(self):
        self.q.get().addCallback(self.wordForward)

    # trigger send
    def wordForward(self, data):
        try:
            self.factory.send(self, data)
            self.q.get().addCallback(self.wordForward)
        except Exception as E:
            print E

    def dataReceived(self, d):
        #self.transport.write(data)
        #self.q.put(data)
        for x in range(0, len(d), 21):
            data = d[x:x+21]
            parsed = unpack("BiiiiB", data[0:21])
            if parsed[0] == 1: #a request for gamemode
                data = pack("BiiiiB", 1, MODE, self.factory.level, 0, 0, 0)
                #if a client asked for something,
                #just give it to them
                toSend = pack("B", self.uid) + data
                self.transport.write(toSend)
                if len(toSend) != 22:
                    print len(toSend)
                self.factory.sendCards(self)
            elif parsed[0] == 2: #a "i collected something" message
                self.factory.collect(parsed[1]) #collect the card
                self.factory.send(self, data)
            elif parsed[0] == 3:
                self.factory.beginReset()
                self.factory.send(self, data)
            else: #otherwise forward it
                self.factory.send(self, data)

# create factor
class ClientConnectionFactory(ClientFactory):
    def __init__(self):
        self.cards = set()
        self.level = int(LEVEL)
        self.count = 1
        self.cons = []
        self.addMore()
        self.resetting = False

    # collect a card (add it to the list)
    def collect(self, n):
        self.cards.add(n)

    # transport a card
    def sendCards(self, who):
        # send the data of which ones are collected
        for n in sorted(list(self.cards)):
            data = pack("BiiiiB", 2, n, 0, 0, 0, 0)
            toSend = pack("B", who.uid) + data
            who.transport.write(toSend)
            if len(toSend) != 22:
                print "1", len(toSend)

    # return the list
    def buildProtocol(self, addr):
        return self.cons[-1]

    # add a connection
    def addMore(self):
        self.cons.append(ClientConnection(self, self.count))
        self.count += 1

    
    # transport wrap the uid and send it 
    # excludes the current person
    def sendMe(self, guy, data):
        for c in self.cons:
            if c.uid != guy.uid:
                toSend = pack("B", c.uid) + data
                guy.transport.write(toSend)
                if len(toSend) != 22:
                    print "2", len(toSend)

    # transfer wrap the buid and send it 
    # excludes the current person from it
    def send(self, guy, data):
        for c in self.cons:
            if c.uid != guy.uid and c.transport:
                #c.transport.write(pack("B", guy.uid) + data)
                toSend = pack("B", guy.uid) + data
                c.transport.write(toSend)
                if len(toSend) != 22:
                    print "3", len(toSend)
        
    # send packets with uid as 0 for when we dont want to exclude the current guy
    def sendall(self, data):
        for c in self.cons:
            if  c.transport:
                #c.transport.write(pack("B", guy.uid) + data)
                toSend = pack("B", 0) + data
                c.transport.write(toSend)
                if len(toSend) != 22:
                    print "3", len(toSend)

    # trigger the reset
    def beginReset(self):
        if not self.resetting:
            self.resetting = True
            Timer(7.5, self.reset).start()

    # actually transmit the reset and change state
    def reset(self):
        print "RESET"
        self.resetting = False
        self.cards = set()
        self.level = 3
        data = pack("BiiiiB", 1, MODE, self.level, 0, 0, 0)
        self.sendall(data)

# start listening
reactor.listenTCP(CLIN_PORT, ClientConnectionFactory())
reactor.run()
