#!/usr/bin/env python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client('')

lcd = Adafruit_CharLCD()

localip = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
wanip = "host myip.opendns.com resolver1.opendns.com | grep 'myip.opendns.com has' | awk '{print $4}'"
ping = "ping -q -c 1 8.8.8.8 | grep rtt | awk '{print $4}' | cut -d/ -f1"
first = 0
count = 0
ping_str = 0

lcd.begin(20, 4)


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

while 1:
    lcd.clear()
    localipaddr = run_cmd(localip)
    wanipaddr = run_cmd(wanip)
    ping_str= run_cmd(ping)
    
    if ping_str != "":

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

#    pingplus = float(pingnum) +1
#    lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
#    lcd.message('LAN IP %s' % (localipaddr))
        lcd.setCursor(0, 0)
        lcd.message('WANIP %s' % (wanipaddr))
#    lcd.setCursor(0, 2)
#    lcd.message('WAN 192.168.100.100')
        lcd.setCursor(0, 1)
        lcd.message('Ping %0.2f' % (pingnum))
        lcd.setCursor(0, 2)
        lcd.message('%0.2f %0.2f %0.2f' % (pingavg, pingmin, pingmax))
        
        aio.send('wan-ip', wanipaddr)
        aio.send('ping', pingnum)
        data0 = aio.receive('wan-ip')
        print('Received value: {0}'.format(data0.value))
        data1 = aio.receive('ping')
        print('Received value: {0}'.format(data1.value))
        
        sleep(2)
