sudo apt install git wget python python-pip python-setuptools -y

cd /home/pi/

git clone https://github.com/HaywardPeirce/Adafruit-Raspberry-Pi-Python-Code.git
cd Adafruit-Raspberry-Pi-Python-Code/
git checkout legacy

cd /home/pi/Pi-Web-Status-Display/
git checkout influx

sudo pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
sudo pip install -r requirements.txt

sudo chmod +x WAN_ping_display.py
sudo cp pidisplay.service /etc/systemd/system/pidisplay.service
sudo systemctl start pidisplay.service

sudo reboot