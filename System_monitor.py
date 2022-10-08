#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.
Needs psutil (+ dependencies) installed::
  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

#if os.name != 'posix':
#    sys.exit('{} platform not supported'.format(os.name))

from oled_device import get_device
from luma.core.render import canvas
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
import subprocess

# try:
#    import psutil
# except ImportError:
#    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
#    sys.exit()


# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


# def bytes2human(n):
#     """
#     >>> bytes2human(10000)
#     '9K'
#     >>> bytes2human(100001221)
#     '95M'
#     """
#     symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
#     prefix = {}
#     for i, s in enumerate(symbols):
#         prefix[s] = 1 << (i + 1) * 10
#     for s in reversed(symbols):
#         if n >= prefix[s]:
#             value = int(float(n) / prefix[s])
#             return '%s%s' % (value, s)
#     return "%sB" % n


# def cpu_usage():
#     # load average, uptime
#     uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
#     av1, av2, av3 = os.getloadavg()
#     return "Ld:%.1f %.1f %.1f Up: %s" \
#         % (av1, av2, av3, str(uptime).split('.')[0])


# def mem_usage():
#     usage = psutil.virtual_memory()
#     return "Mem: %s %.0f%%" \
#         % (bytes2human(usage.used), 100 - usage.percent)


# def disk_usage(dir):
#     usage = psutil.disk_usage(dir)
#     return "SD:  %s %.0f%%" \
#         % (bytes2human(usage.used), usage.percent)


# def network(iface):
#     stat = psutil.net_io_counters(pernic=True)[iface]
#     return "%s: Tx%s, Rx%s" % \
#            (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))
def parserOutput(strinput):
    index = strinput.find("b'")
    if index == 0:
        strinput = strinput.replace("b'",'')
        strinput = strinput[:-1]
    return strinput

def stats(device):
    with canvas(device) as draw:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usag>
        cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
        IP = subprocess.check_output(cmd, shell = True ).decode(sys.stdout.encoding)

#       cmd = "top -bn1 | grep load | awk '{printf \"CPU %.2f%\", $(NF-2)}'"
        cmd = "top -bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\([0-9.]*\)%* id.*/\\1/\" | awk '{printf \"CPU %s%\", 100 - $1}'"
        CPU = subprocess.check_output(cmd, shell = True ).decode(sys.stdout.encoding)

#       cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"
        cmd = "free -m | awk 'NR==2{printf \"%sMB\", $3}'"
        MemUsage = subprocess.check_output(cmd, shell = True).decode(sys.stdout.encoding)

        cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
        cmd = "df -h | awk '$NF==\"/\"{printf \"%s\", $5}'"
        Disk = subprocess.check_output(cmd, shell = True ).decode(sys.stdout.encoding)

        cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
        Temperature = subprocess.check_output(cmd, shell = True ).decode(sys.stdout.encoding)

# Icons
# Icon temperator
        draw.text((x, top+4), chr(62152), font=font_icon, fill=255)
# Icon memory
        draw.text((x+60, top+4), chr(62171), font=font_icon, fill=255)
# Icon disk
        draw.text((x, top+30), chr(61888),  font=font2, fill=255)
# Icon Wifi
        draw.text((x, top+52), chr(61931),  font=font2, fill=255)

# Text temperature
        draw.text((x+17, top+7), str(Temperature), font=font, fill=255)
# Text mem usage
        draw.text((x+80, top+7), str(MemUsage), font=font, fill=255)
# Text Disk usage
        draw.text((x+17, top+30), str(Disk), font=font, fill=255)
# Text cpu usage
        draw.text((x+60, top+30), str(CPU), font=font, fill=255)

# Text IP addresss
        draw.text((x+18, top+52), str(IP), font=font_text_small, fill=255)


def main():
    while True:
        stats(device)
        time.sleep(2)


if __name__ == "__main__":
    try:
        device = get_device()
        font = ImageFont.truetype('ChiKareGo.ttf', 16)
        font2 = ImageFont.truetype('fontawesome-webfont.ttf', 14)
        font_icon = ImageFont.truetype('fontawesome-webfont.ttf', 20)
        font_text_small = ImageFont.truetype('FreePixel.ttf', 14)
        width = device.width
        height = device.height
        padding = -2
        top = padding
        bottom = height - padding
        x = 0
        main()
    except KeyboardInterrupt:
        pass
