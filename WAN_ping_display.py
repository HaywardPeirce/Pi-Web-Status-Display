#!/usr/bin/env python

import os, sys, os.path
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import highping
import temperature

#from Adafruit_CharLCD import Adafruit_CharLCD
#/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCD

import imp

Adafruit_CharLCD = imp.load_source('Adafruit_CharLCD', '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCD/Adafruit_CharLCD.py')

from Adafruit_CharLCD import Adafruit_CharLCD

#Read the Adafruit API key in from file /home/pi/apikey.txt.
file = open('./apikey.txt', 'r')
apikey = file.readline().replace("\n", '')
file.close()

# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client(apikey)

lcd = Adafruit_CharLCD()

localip = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
wanip = "host myip.opendns.com resolver1.opendns.com | grep 'myip.opendns.com has' | awk '{print $4}'"
ping = "ping -q -c 1 8.8.8.8 | grep rtt | awk '{print $4}' | cut -d/ -f1"
first = 0
count = 0
ping_str = 0
localtemp = None

lcd.begin(20, 4)

#run a CLI command
def run_cmd(cmd):
    try:
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output
    except:
        e = sys.exc_info()[0]
        print("Unable to run command: {}".format(e))
        return None

while 1:
    
    #lookup each of the CLI values
    localipaddr = run_cmd(localip)
    wanipaddr = run_cmd(wanip)
    ping_str = run_cmd(ping)
    
    if ping_str and localipaddr and wanipaddr:

    	pingnum = float(run_cmd(ping))
    	if first == 0:
	        pingavg = pingnum
	        pingmin = pingnum
	        pingmax = pingnum
	        first = 1

        count = count + 1
        if count > 1:
	        pingavg = (pingavg * (count - 1) / count) + (pingnum / count)
        if pingnum > pingmax:
	        pingmax = pingnum
        if pingnum < pingmin:
	        pingmin = pingnum
	    
        #send the ping value to the highping function
        if pingnum > 100:
            highping.main(pingnum)
	    
        #find the local temp, using the openweathermap city ID
        tempTemp = temperature.local(6174041)
        
        #make sure that the temp was able to be looked up
        if tempTemp:
            localtemp = tempTemp
	    
        tempTemp = temperature.room(apikey, 'temperature')
        
        if tempTemp:
            roomtemp = tempTemp
        
        lcd.clear()
	    
        lcd.setCursor(0, 0)
        lcd.message('WANIP %s' % (wanipaddr))

        lcd.setCursor(0, 1)
        lcd.message('Ping %0.2f' % (pingnum))
        lcd.setCursor(0, 2)
        lcd.message('%0.2f %0.2f %0.2f' % (pingavg, pingmin, pingmax))
        lcd.setCursor(0, 3)
        lcd.message('temp:%0.1f room:%0.1f' % (localtemp, roomtemp))
        
        try:
            aio.send('wan-ip', wanipaddr)
        except:
            e = sys.exc_info()[0]
            print("Error sending 'wan-ip' value: {}".format(e))
        try:
            aio.send('ping', pingnum)
        except:
            e = sys.exc_info()[0]
            print("Error sending 'ping' value: {}".format(e))
        try:
            data0 = aio.receive('wan-ip')
            print('Received value: {0}'.format(data0.value))
        except:
            e = sys.exc_info()[0]
            print("Error recieving 'wan-ip' value: {}".format(e))
        try:
            data1 = aio.receive('ping')
            print('Received value: {0}'.format(data1.value))
        except:
            e = sys.exc_info()[0]
            print("Error recieving 'ping' value: {}".format(e))
        
        sleep(10)
