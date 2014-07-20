#!/usr/bin/env python

from twisted.internet import reactor, protocol
from rc4 import encrypt

key = "1234567890"


class EchoClient(protocol.Protocol):
   def connectionMade(self):
       #self.transport.write("Hello, world!")
       gpsdata = "$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D"
       enc = encrypt(gpsdata, key)
       self.transport.write(enc)
       #self.transport.write(data)

   def dataReceived(self, data):
       print "Server said:", data
       self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
   def buildProtocol(self, addr):
       return EchoClient()

   def clientConnectionFailed(self, connector, reason):
       print "Connection failed."
       reactor.stop()

   def clientConnectionLost(self, connector, reason):
       print "Connection lost."
       reactor.stop()

reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()
