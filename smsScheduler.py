#!/usr/bin/env python

import sys
import MySQLdb as mdb
import logging

con = mdb.connect('localhost', 'root', '123456', 'smsd');

phoneNumber = str(sys.argv[1])
imei = str(sys.argv[2])
with con:
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM gpslog ORDER BY id DESC LIMIT 0,1")
    rowsgps = cur.fetchall()

    for rowgps in rowsgps:
        gps_lat = rowgps['lat']
        gps_lon = rowgps['lon']

gpsdata = "%s,%s,%s" % (imei,gps_lat,gps_lon)
sql = "INSERT INTO outbox(DestinationNumber, TextDecoded, creatorID) VALUES('%s','%s','Gammu')" % (phoneNumber, gpsdata);
print sql
cur.execute(sql)
con.commit()

#cur.execute(sql)
#        cur.execute(sql1)
#        con.commit()


