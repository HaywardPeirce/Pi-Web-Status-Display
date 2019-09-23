#!/usr/bin/env python

import os, sys, os.path, json, configparser
from subprocess import *
from time import sleep, strftime
from datetime import datetime
# import highping
# import temperature

config = configparser.ConfigParser()
config.read('config.ini')

delay = float(config['GENERAL']['Delay'])
output = bool(config['GENERAL'].get('Output', fallback=True))

from influxdb import InfluxDBClient

influxAddress = config['INFLUXDB']['Address']
influxPort = float(config['INFLUXDB']['Port'])
influxUser = config['INFLUXDB'].get('Username', fallback='')
influxPassword = config['INFLUXDB'].get('Password', fallback='')

# TODO: setup config entries for table and value names for each of the influx queries

roomTempDB = config['INFLUXDB'].get('roomtempdb', fallback='weather')
roomTempValue = config['INFLUXDB'].get('roomtempvalue', fallback='temperature')
localTempDB = config['INFLUXDB'].get('localtempdb', fallback='weather')
localTempValue = config['INFLUXDB'].get('localtempvalue', fallback='temperature')
localTempID = config['INFLUXDB'].get('localTempID', fallback='29')
pingDB = config['INFLUXDB'].get('pingdb', fallback='speedtest')
pingValue = config['INFLUXDB'].get('pingvalue', fallback='ping')

influx_client = InfluxDBClient(influxAddress, influxPort, influxUser, influxPassword)

client = InfluxDBClient('192.168.1.167', 8086, 'root', 'root', 'example')

#from Adafruit_CharLCD import Adafruit_CharLCD
#/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCD

import imp

Adafruit_CharLCD = imp.load_source('Adafruit_CharLCD', '/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCD/Adafruit_CharLCD.py')
from Adafruit_CharLCD import Adafruit_CharLCD

#Read the Adafruit API key in from file /home/pi/apikey.txt.
# file = open('/home/pi/Pi-Web-Status-Display/apikey.txt', 'r')
# apikey = file.readline().replace("\n", '')
# file.close()

# Import library and create instance of REST client.
# from Adafruit_IO import Client
# aio = Client(apikey)

lcd = Adafruit_CharLCD()

localip = "ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
wanip = "host myip.opendns.com resolver1.opendns.com | grep 'myip.opendns.com has' | awk '{print $4}'"
# ping = "ping -q -c 1 8.8.8.8 | grep rtt | awk '{print $4}' | cut -d/ -f1"
# first = 0
# count = 0
# ping_str = 0
# localtemp = None

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

def lookupInfluxValue(query):

    if query == "roomTemp":
        client.switch_database('weather')

        queryString = 'SELECT last("' + roomTempValue + '") FROM "' + roomTempDB + '"'

        results = client.query(queryString)
        points = results.get_points()

        temp = None
        for point in points:

            print(point["last"])
            temp = float(point["last"])

        return temp

    elif query == "localTemp":

        client.switch_database('weather')
        queryString = 'SELECT last("' + localTempValue + '") FROM "' + localTempDB + '" WHERE ("stationId" = '+ "'" + localTempID +"'" +')'

        results = client.query(queryString)
        points = results.get_points()

        temp = None
        for point in points:

            print(point)
            temp = float(point["last"])

        return temp

    elif query == "ping":

        client.switch_database('speedtests')

        # results = client.query('SELECT last("temperature") FROM "housetemps" WHERE time > now() - 5m')
        results = client.query('SELECT "' + pingTempValue + '" FROM "' + pingDB + '" WHERE time > now() - 1h')
        points = results.get_points()

        last = None
        pings = []

        for point in points:

            pings.append(point['ping'])
            last = point['ping']

        pingInfo = {}
        pingInfo['ping'] = last
        pingInfo['pingavg'] = sum(pings)/len(pings)
        pingInfo['pingmax'] = max(pings)
        pingInfo['pingmin'] = min(pings)

        return pingInfo

    else: return None
    
def main():
    
    #lookup each of the CLI values
    # localipaddr = run_cmd(localip)
    
    wanipaddr = None
    
    try:
        wanipaddr = run_cmd(wanip)
    except:
        print("Unable to retrieve WAN IP address.")
    
    try:
        roomTemp = lookupInfluxValue("roomTemp")
        localTemp = lookupInfluxValue("localTemp")

        pingInfo = lookupInfluxValue("ping")
    except:
        print("Unable to retrieve values from InfluxDB")

    try:

        lcd.clear()
        
        lcd.setCursor(0, 0)
        lcd.message('WANIP %s' % (wanipaddr))

        lcd.setCursor(0, 1)
        lcd.message('Ping %0.2f' % (pingInfo['ping']))
        lcd.setCursor(0, 2)
        lcd.message('%0.2f %0.2f %0.2f' % (pingInfo['pingavg'], pingInfo['pingmin'], pingInfo['pingmax']))
        lcd.setCursor(0, 3)
        lcd.message('temp:%0.1f room:%0.1f' % (localTemp, roomTemp))

    except:
        print("Unable to display data to screen.")
    
    sleep(delay)

if __name__ == '__main__':
    main()