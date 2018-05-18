import requests, sys, json
from Adafruit_IO import Client

file = open('/home/pi/Pi-Web-Status-Display/weatherapikey.txt', 'r')

weatherapikey = file.readline().replace("\n", '')

file.close()

def main():
    print 'main'
    
    #response = requests.get(requestURL)
    
    #return response.json()['main']['temp']-273.15
    
def local(cityid):
    
    #try looking up the temerature from openweathermap
    try:
    
        requestURL = 'http://api.openweathermap.org/data/2.5/weather?id=' + str(cityid) + '&APPID=' + weatherapikey
    
        response = requests.get(requestURL)
    
        return response.json()['main']['temp']-273.15
    
    #if the temp from open weather map can't be found then return None
    except: 
        e = sys.exc_info()[0]
        print("Could not retrieve temperature for openweathermap city ID {}: {}".format(cityid, e))
        return None
    
def room(apikey, *feeds):
    
    temp = []
    
    aio = Client(apikey)
    
    for feed in feeds:
        try:
            iotemp = aio.receive(feed)
            temp.append(float(iotemp.value))
        except: print("Could not retrieve temperature for feed {}".format(feed))
    
    #if any room temp values were able to be looked up        
    if temp:
        roomtemp = sum(temp)/len(temp)
        return roomtemp
    else: return None