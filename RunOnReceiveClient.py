#/usr/bin/env python

import smsParser
import ConfigParser
import MySQLdb as mdb
import sys
import smsParser
from crontab import CronTab
 
tab = CronTab()
cmdx = '/home/pi/smsmScheduler.py'


con = mdb.connect('localhost', 'root', '123456', 'smsd');
Config = ConfigParser.ConfigParser()
Config.read("clientconfig.cfg")
gpsdata = ""
with con:

    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM inbox WHERE processed='false'")

    rows = cur.fetchall()

    for row in rows:
        smsid = row["ID"]
        phoneNumber = row["SenderNumber"]
        text = row["TextDecoded"]
      
 
    cur.execute("SELECT * FROM gpslog ORDER BY id DESC LIMIT 0,1")
    rowsgps = cur.fetchall()

    for rowgps in rowsgps:
        gps_lat = rowgps['lat']
        gps_lon = rowgps['lon']
        #print rowgps[1]

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

telp = ConfigSectionMap("client-config")['telp']
#print "client telp : %s." % (telp)

version = ConfigSectionMap("client-config")['version']
#print "client version : %s." % (version)

sn = ConfigSectionMap("client-config")['sn']
#print "serial number : %s." % (sn)

password = ConfigSectionMap("client-config")['password']
#print "client pass : %s." % (password)

imei = ConfigSectionMap("client-config")['imei']
#print "client imei : %s." % (imei)
	
#smsParser.test()
#text = ""
#text = "W000000,000"
#text = "W******,001"
#text = "W******,001,######"
#text = "W******,002"
text = "W000000,002,000"
#text = "W******,003"
#text = "W******,003,1"
#text = "W******,003,1,1,TelNumber"
#text = "W000000,600"
#text = "W000000,601"
#print text
#Err SMS
Err = "Error, hacking attempt"

cmd = smsParser.splitter(text)
#gpsdata="@@,LL,%f,%f" % (gps_lat,gps_lon)
gpsdata = "https://www.google.co.id/maps/preview/@%f,%f,15z" % (gps_lat,gps_lon)

def smsReply(str):
    print str
	
#TODO get user password
def getconfigpasswd():
    #cfgpass = "######"
    #cfgpass = "******"
    cfgpass = ConfigSectionMap("client-config")['password']
    return cfgpass
	
def getsmspasswd(str_cmd):
    return str_cmd[1:7]
    #print pwd

def checkpasswd(str_cmd):
    cfgpwd = getconfigpasswd()
    smspwd = getsmspasswd(str_cmd)
    if cfgpwd <> smspwd:
        return False
    else:
        return True
		
#def list_sms_cmd(cmd):
#    for x in range(0, len(cmd)):
#        print "command %s " % (cmd[x])
		
def func_000(cmd):
    #print "Get Current Location"
    if checkpasswd(cmd[0]):
        print "Get Current Location OK!"
        #send reply SMS Current Location
        #smsReply(gpsdata)
        sql = "INSERT INTO outbox(DestinationNumber, TextDecoded, creatorID) VALUES('%s','%s','Gammu')" % (phoneNumber, gpsdata);
        print sql
        cur.execute(sql)
        sql1 = "UPDATE inbox SET Processed = 'true' WHILE ID=%d" % (smsid);
        print sql1
        cur.execute(sql1)
        con.commit()

    else:
        print "Error, wrong password"
		#send reply SMS Error
        smsReply(Err)
		
def	func_001(cmd):
    #print "Change User password"
    if checkpasswd(cmd[0]):
        try:
            #int(cmd[2])
            print "Change password OK!"
            smsReply("OK!")
			#send reply SMS OK
        except IndexError:
            print "Error, New 6 digit key required!"
            smsReply(Err)
			#send reply SMS Error
    else:
        print "Error, wrong password"
        smsReply(Err)
		#send reply SMS Error
		
def func_002(cmd):
    #print "Set interval for automatic timed report"
    if checkpasswd(cmd[0]):
        try:
            minit=int(cmd[2])
            if minit == 0:
                cmdx1 = cmdx+' '+phoneNumber+' '+imei
                cron_job = tab.find_command(cmdx1)
                #if len(cron_job) > 0:
                tab.remove_all(cmdx) 
                #    #writes content to crontab
                tab.write()
                print "Stop Sending!"
            else:
                print minit
                cmdx1 = cmdx+' '+phoneNumber+' '+imei
                cron_job = tab.new(cmdx1)
                cron_job.minute.every(minit)
                tab.write()
                print tab.render()

                print "Set %d interval for automatic timed report OK!" % minit
            
            #print "Set interval for automatic timed report OK!"
            smsReply("Set ATR OK!")
            
        except IndexError:
            print "Error, number for automatic timed report not set "
            #send reply SMS Error
            smsReply(Err)			
    else:
        print "Error, wrong password"
        #send reply SMS Error
        smsReply(Err) 		
        			    
def func_003(cmd):
    #print ("Set preset phone number for SOS button ")
    if checkpasswd(cmd[0]):
        try:
            cmd[2]
            cmd[3]
            cmd[4]
            print "Set preset phone number for SOS button OK!"
            smsReply("set preset phone number OK!")
        except IndexError:
            print "Error, preset phone number for SOS button not set"
            smsReply(Err)
			#send reply SMS Error
    else:
        print "Error, wrong password"
        #send reply SMS Error
        smsReply(Err)
		
#def func_004(cmd):
#    list_sms_cmd(cmd)
#    print ("Set low power alert")

def func_600(cmd):
    if checkpasswd(cmd[0]):
        #print ("Get IMEI")
        print ("Get IMEI OK!")
        #send reply SMS OK
        sql = "INSERT INTO outbox(DestinationNumber, TextDecoded, creatorID) VALUES('%s','%s','Gammu')" % (phoneNumber, imei);
        print sql
        sql1 = "UPDATE inbox SET Processed = 'true' WHILE ID=%d" % (smsid);
        print sql1
        #smsReply(imei)
    else:
        print "Error, wrong password"
        #send reply SMS Error
        smsReply(Err)
		
def func_601(cmd):
    if checkpasswd(cmd[0]):
        #print ("Get version and serial number")
        print ("Get version and serial number OK!")
		#send reply SMS version and serial number
        #sn = ConfigSectionMap("client-config")['sn']
        sql = "INSERT INTO outbox(DestinationNumber, TextDecoded, creatorID) VALUES('%s','%s','Gammu')" % (phoneNumber, sn);
        print sql
        cur.execute(sql)
        sql1 = "UPDATE inbox SET Processed = 'true' WHILE ID=%d" % (smsid);
        print sql1
        cur.execute(sql1)
        con.commit()
        #smsReply(sn)

    else:
        print "Error, wrong password"
        #send reply SMS Error
        smsReply(Err)

#python style switch for switching command function    	
switch = {'000': func_000,
    '001': func_001,
    '002': func_002,
	'003': func_003,
#	'004': func_004,
	'600': func_600,
	'601': func_601,
    }

if len(cmd) > 1:
    if cmd[1] in switch:
        switch[cmd[1]](cmd)
    else:
        pass
        #default
else:
    print "Error, no command!"
