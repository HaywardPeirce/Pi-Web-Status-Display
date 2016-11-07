# Pi-Web-Status-Display
A Raspberry Pi-based project for tracking and displaying certain network metrics.

Currently the system keeps track of the:

- WAN address
- Ping time to 8.8.8.8
- Min Ping
- Average Ping
- Max Ping

THe metrics are then displayed on an HDD44780 compatible LCD and through Adafruit.io

### Resources
THe main reference for this project was the Adafruit LCD guide: https://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi/overview

The python code used to drive the diaplay uses Adafruits LCD library. For a combination of reasons (could be the older Pi being used, or the more obscure 20x4 LCD) the legacy branch of the older LCD library was what I managed to get working on my screen: https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/legacy

Information on how to create an Upstart Service was found here: https://stackoverflow.com/questions/17747605/daemon-vs-upstart-for-python-script

Details about including Adafruit.io were found here: https://github.com/adafruit/io-client-python

### Installation
Follow the Adafruit installation guide for wiring and testing out the display

Place the python script you want to run in the `Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCD/` directory. You can place it elsewhere but you will have to reference the python library `Adafruit_CharLCD` by its absolute path

Place the Adafruit APIkey in a files in the pi user home directory called apikey.txt

Install Upstart with: `sudo apt-get install upstart`

Place the networktestservice.conf file in /etc/init

Reboot the Pi


