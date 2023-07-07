# Pi-hole
Pi-hole installation instructions

# Install the OS
Raspberry Pi OS Lite (32 bit)


# Update the OS
sudo apt-get update

sudo apt-get upgrade


# Install Pi-hole
curl -sSL https://install.pi-hole.net | bash

Use Canadian Shield DNS: https://www.cira.ca/cybersecurity-services/canadian-shield/configure/summary-cira-canadian-shield-dns-resolver-addresses:

149.112.121.20, 149.112.122.20


# Setup Adafruit Mini PiTFT - 135x240 Color TFT Add-on for Raspberry Pi
https://learn.adafruit.com/pi-hole-ad-blocker-with-pi-zero-w?view=all#install-mini-pitft

https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup

sudo apt-get install python3-pip

sudo apt-get install fonts-dejavu

sudo apt-get install python3-pil    #-----> Not needed

sudo apt-get install python3-numpy     #-----> Not needed

sudo pip3 install --upgrade adafruit-blinka adafruit-circuitpython-rgb-display spidev

# Stats.py
sudo nano /etc/pihole_stats.py

Changed the font size to 16:
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

Added my pi-hole API key:
API_TOKEN = "123456789.............."

sudo nano /etc/rc.local

Add on the line before exit:

  sleep 10
  
  sudo python3 /etc/pihole_stats.py &

# Enable SPI
https://raspberrypi.stackexchange.com/questions/127793/raspberry-pi-4b-no-dev-spidev0-0

https://pimylifeup.com/raspberry-pi-spi/

  sudo raspi-config nonint do_spi 0
  
  OR

  sudo nano /boot/config.txt
  
    uncomment #dtparam=spi=on

# Reboot
sudo reboot

Voilà!
