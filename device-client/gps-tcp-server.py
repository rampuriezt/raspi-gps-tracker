#!/usr/bin/env python

from twisted.internet import protocol, reactor
from rc4 import decrypt
import pynmea2
import datetime
#import gpslog

key ="1234567890"
imei = "123456789012345"

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        plain = decrypt(data,key)        
        
        print plain
        
        msg = pynmea2.parse(plain)
        sql = "INSERT INTO gpsdata (imei,latitude,longitude,date_time)"
        sql += " VALUES ('%s', %f, %f, '%s')" % (imei,msg.latitude,msg.longitude,msg.timestamp)
        
        print "data terencrypt : %s" % data
        print "data plain : %s " % plain
        print "QUERY SQL :%s" % sql
        
        #print msg.datestamp
        #print msg.longitude

        self.transport.write("OK")
        

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()
