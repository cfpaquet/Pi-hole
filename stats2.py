# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-
# Import Python System Libraries
import time
import json
import subprocess

# Import Requests Library
import requests

#Import Blinka
import digitalio
import board

# Import Python Imaging Library
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

API_TOKEN = "YOUR_API_TOKEN_HERE"
api_url = "http://localhost/admin/api.php?summaryRaw&auth="+API_TOKEN

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE,
                     width=135, height=240, x_offset=53, y_offset=40)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width   # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new('RGB', (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Add buttons as inputs
buttonA = digitalio.DigitalInOut(board.D23)
buttonA.switch_to_input()

buttonB = digitalio.DigitalInOut(board.D24)
buttonB.switch_to_input()

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = "IP: "+subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/net/wlan0/address"
    MAC = "MAC: "+subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "hostname | tr -d \'\\n\'"
    HOST = subprocess.check_output(cmd, shell=True).decode("utf-8")+".local"
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/thermal/thermal_zone0/temp | awk '{print \"Temp(C): \" $0/1000}'"
    TEMP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "uptime -p| awk '{print \"Uptime: \" $0}'"
    UPTIME = subprocess.check_output(cmd, shell=True).decode("utf-8")
   
    # Pi Hole data!
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        DNSQUERIES = data['dns_queries_today']
        ADSBLOCKED = data['ads_blocked_today']
        ADSBLOCKPCT = data['ads_percentage_today']
        CLIENTS = data['unique_clients']
        BLOCKLIST = data['domains_being_blocked']
        STATUS = data['status']
    except KeyError:
        time.sleep(1)
        continue

    y = top
    if not buttonA.value:  # just button A pressed
        draw.text((x, y), HOST, font=font, fill="#FFFF00")
        y += font.getsize(HOST)[1]
        draw.text((x, y), IP, font=font, fill="#FFFF00")
        y += font.getsize(IP)[1]
        draw.text((x, y), MAC, font=font, fill="#FFFF00")
        y += font.getsize(MAC)[1]
        draw.text((x, y), CPU, font=font, fill="#FFFF00")
        y += font.getsize(CPU)[1]
        draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        y += font.getsize(MemUsage)[1]
        draw.text((x, y), Disk, font=font, fill="#0000FF")
        y += font.getsize(Disk)[1]
        draw.text((x, y), TEMP, font=font, fill="#0000FF")
        y += font.getsize(TEMP)[1]
        draw.text((x, y), UPTIME, font=font, fill="#0000FF")
        y += font.getsize(UPTIME)[1]
    else:
        draw.text((x, y), HOST, font=font, fill="#FFFF00")
        y += font.getsize(HOST)[1]
        draw.text((x, y), IP, font=font, fill="#FFFF00")
        y += font.getsize(IP)[1]
        draw.text((x, y), MAC, font=font, fill="#FFFF00")
        y += font.getsize(MAC)[1]
        draw.text((x, y), "Ads Blocked: {}".format(str(ADSBLOCKED)) + "(" + str(ADSBLOCKPCT) + "%)", font=font, fill="#00FF00")
        y += font.getsize(str(ADSBLOCKED))[1]
        draw.text((x, y), "DNS Queries: {}".format(str(DNSQUERIES)), font=font, fill="#FF00FF")
        y += font.getsize(str(DNSQUERIES))[1]
        draw.text((x, y), "Clients: {}".format(str(CLIENTS)), font=font, fill="#0000FF")
        y += font.getsize(str(CLIENTS))[1]
        draw.text((x, y), "Domains on blocklist: {}".format(str(BLOCKLIST)), font=font, fill="#0000FF")
        y += font.getsize(str(BLOCKLIST))[1]
        draw.text((x, y), "Status: {}".format(str(STATUS)), font=font, fill="#0000FF")
        y += font.getsize(str(STATUS))[1]
  
    # Display image.
    disp.image(image, rotation)
    time.sleep(.1)

    if not buttonB.value:  # just button B pressed
       draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
       disp.image(image, rotation)
       subprocess.run("shutdown now", shell=True)
