#!/usr/bin/python

import sys
import os
import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket
from subprocess import check_output

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    # font24 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 24)
    font24 = ImageFont.truetype('Font.ttc', 24)
    ipAddr = str(check_output(['hostname', '-I']))
    ipAddr = ipAddr.split('\'')[1].split(' ')[0]
    
    logging.info("ipaddr: " + ipAddr)

    logging.info("\"Hello World!\"ing")
    epd.init_fast()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'Hello World', font = font24, fill = 0)
    draw.text((10, 20), ipAddr, font = font24, fill = 0)
    epd.display(epd.getbuffer(Himage))
    
    time.sleep(4)
    
    logging.info("Clear...")
    epd.init()
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()

