#!/usr/bin/python

from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont

epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()
epd.sleep()
