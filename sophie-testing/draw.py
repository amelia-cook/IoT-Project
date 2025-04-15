#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
from subprocess import check_output

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 18)
    font10 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 10)

    ipAddr = str(check_output(['hostname', '-I']))
    ipAddr = ipAddr.split('\'')[1].split(' ')[0]
    logging.info("ipaddr: " + ipAddr)

    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...")
    epd.init_fast()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    notes_count = 4

    if notes_count == 1:
        draw.text((20, 20), 'DAILY CALENDAR', font = font24, fill = 0)
        draw.text((709,450), ipAddr , font = font10, fill = 0)
        draw.rectangle((10, 10, 789,469), outline = 0)
        draw.line((20,50, 779,50), fill = 0)

        draw.text((20,55), 'event1', font = font18, fill = 0)
        draw.text((20,80), 'event2', font = font18, fill = 0)
        draw.text((20,105), 'event3', font = font18, fill = 0)
        draw.text((20,130), 'event4', font = font18, fill = 0)
        draw.text((20,155), 'event5', font = font18, fill = 0)
        draw.text((20,180), 'event6', font = font18, fill = 0)
        draw.text((20,205), 'event7', font = font18, fill = 0)
        draw.text((20,230), 'event8', font = font18, fill = 0)
        draw.text((20,255), 'event9', font = font18, fill = 0)
        draw.text((20,280), 'event10', font = font18, fill = 0)
        draw.text((20,305), 'event11', font = font18, fill = 0)
        draw.text((20,330), 'event12', font = font18, fill = 0)
        draw.text((20,355), 'event13', font = font18, fill = 0)
        draw.text((20,380), 'event14', font = font18, fill = 0)
        draw.text((20,405), 'event15', font = font18, fill = 0)
        draw.text((20,430), 'event16', font = font18, fill = 0)
        
    elif notes_count == 3:
        draw.text((20, 20), 'DAILY CALENDAR', font = font24, fill = 0)
        draw.text((414, 255), 'Get this shtuff done less ASAP', font = font24, fill = 0)
        draw.text((414, 20), 'Get this shtuff done ASAP', font = font24, fill = 0)
        draw.text((320,450), ipAddr , font = font10, fill = 0)

        draw.rectangle((10, 10, 394, 469), outline = 0)
        draw.rectangle((404, 10, 789,234), outline = 0)
        draw.rectangle((404, 244, 789, 469), outline = 0)

        draw.line((20,50, 390, 50 ), fill = 0) 
        draw.line((414, 50, 780, 50), fill = 0)
        draw.line((414, 285, 780,285), fill = 0)

        draw.text((20,55), 'event1', font = font18, fill = 0)
        draw.text((20,80), 'event2', font = font18, fill = 0)
        draw.text((20,105), 'event3', font = font18, fill = 0)
        draw.text((20,130), 'event4', font = font18, fill = 0)
        draw.text((20,155), 'event5', font = font18, fill = 0)
        draw.text((20,180), 'event6', font = font18, fill = 0)
        draw.text((20,205), 'event7', font = font18, fill = 0)
        draw.text((20,230), 'event8', font = font18, fill = 0)
        draw.text((20,255), 'event9', font = font18, fill = 0)
        draw.text((20,280), 'event10', font = font18, fill = 0)
        draw.text((20,305), 'event11', font = font18, fill = 0)
        draw.text((20,330), 'event12', font = font18, fill = 0)
        draw.text((20,355), 'event13', font = font18, fill = 0)
        draw.text((20,380), 'event14', font = font18, fill = 0)
        draw.text((20,405), 'event15', font = font18, fill = 0)
        draw.text((20,430), 'event16', font = font18, fill = 0)
    
        draw.text((414,55), 'task1', font = font18, fill = 0)
        draw.text((414,80), 'task2', font = font18, fill = 0)
        draw.text((414,105), 'task3', font = font18, fill = 0)
        draw.text((414,130), 'task4', font = font18, fill = 0)
        draw.text((414,155), 'task5', font = font18, fill = 0)
        draw.text((414,180), 'task6', font = font18, fill = 0)
        draw.text((414,205), 'task7', font = font18, fill = 0)

        draw.text((414,290), 'task1', font = font18, fill = 0)
        draw.text((414,315), 'task2', font = font18, fill = 0)
        draw.text((414,340), 'task3', font = font18, fill = 0)
        draw.text((414,365), 'task4', font = font18, fill = 0)
        draw.text((414,390), 'task5', font = font18, fill = 0)
        draw.text((414,415), 'task6', font = font18, fill = 0)
        draw.text((414,440), 'task7', font = font18, fill = 0)

    elif notes_count == 4:
        draw.text((20, 255), 'Random Note', font = font24, fill = 0)
        draw.text((20, 20), 'DAILY CALENDAR', font = font24, fill = 0)
        draw.text((414, 255), 'Get this shtuff done less ASAP', font = font24, fill = 0)
        draw.text((414, 20), 'Get this shtuff done ASAP', font = font24, fill = 0)
        draw.text((320,220), ipAddr , font = font10, fill = 0)

        draw.rectangle((10, 10, 394, 234), outline = 0)
        draw.rectangle((10, 244, 394, 469), outline = 0)
        draw.rectangle((404, 10, 789,234), outline = 0)
        draw.rectangle((404, 244, 789, 469), outline = 0)

        draw.line((20,50, 384, 50 ), fill = 0)
        draw.line((20,285, 384, 284 ), fill = 0)
        draw.line((414, 50, 780, 50), fill = 0)
        draw.line((414, 285, 780,285), fill = 0)

        draw.text((20,55), 'event1', font = font18, fill = 0)
        draw.text((20,80), 'event2', font = font18, fill = 0)
        draw.text((20,105), 'event3', font = font18, fill = 0)
        draw.text((20,130), 'event4', font = font18, fill = 0)
        draw.text((20,155), 'event5', font = font18, fill = 0)
        draw.text((20,180), 'event6', font = font18, fill = 0)
        draw.text((20,205), 'event7', font = font18, fill = 0)

        draw.text((20,290), 'task1', font = font18, fill = 0)
        draw.text((20,315), 'task2', font = font18, fill = 0)
        draw.text((20,340), 'task3', font = font18, fill = 0)
        draw.text((20,365), 'task4', font = font18, fill = 0)
        draw.text((20,390), 'task5', font = font18, fill = 0)
        draw.text((20,415), 'task6', font = font18, fill = 0)
        draw.text((20,440), 'task7', font = font18, fill = 0)
        
        draw.text((414,55), 'task1', font = font18, fill = 0)
        draw.text((414,80), 'task2', font = font18, fill = 0)
        draw.text((414,105), 'task3', font = font18, fill = 0)
        draw.text((414,130), 'task4', font = font18, fill = 0)
        draw.text((414,155), 'task5', font = font18, fill = 0)
        draw.text((414,180), 'task6', font = font18, fill = 0)
        draw.text((414,205), 'task7', font = font18, fill = 0)

        draw.text((414,290), 'task1', font = font18, fill = 0)
        draw.text((414,315), 'task2', font = font18, fill = 0)
        draw.text((414,340), 'task3', font = font18, fill = 0)
        draw.text((414,365), 'task4', font = font18, fill = 0)
        draw.text((414,390), 'task5', font = font18, fill = 0)
        draw.text((414,415), 'task6', font = font18, fill = 0)
        draw.text((414,440), 'task7', font = font18, fill = 0)


    elif notes_count == 2:
        draw.text((20, 20), 'DAILY CALENDAR', font = font24, fill = 0)
        draw.text((414, 20), 'Get this shtuff done ASAP', font = font24, fill = 0)
        draw.text((320,450), ipAddr , font = font10, fill = 0)

        draw.rectangle((10, 10, 394, 469), outline = 0)
        draw.rectangle((404, 10, 789,469), outline = 0)

        draw.line((20,50, 384, 50 ), fill = 0) 
        draw.line((414, 50, 780, 50), fill = 0)

        draw.text((20,55), 'event1', font = font18, fill = 0)
        draw.text((20,80), 'event2', font = font18, fill = 0)
        draw.text((20,105), 'event3', font = font18, fill = 0)
        draw.text((20,130), 'event4', font = font18, fill = 0)
        draw.text((20,155), 'event5', font = font18, fill = 0)
        draw.text((20,180), 'event6', font = font18, fill = 0)
        draw.text((20,205), 'event7', font = font18, fill = 0)
        draw.text((20,230), 'event8', font = font18, fill = 0)
        draw.text((20,255), 'event9', font = font18, fill = 0)
        draw.text((20,280), 'event10', font = font18, fill = 0)
        draw.text((20,305), 'event11', font = font18, fill = 0)
        draw.text((20,330), 'event12', font = font18, fill = 0)
        draw.text((20,355), 'event13', font = font18, fill = 0)
        draw.text((20,380), 'event13', font = font18, fill = 0)
        draw.text((20,405), 'event14', font = font18, fill = 0)
        draw.text((20,430), 'event15', font = font18, fill = 0)
    
        draw.text((414,55), 'task1', font = font18, fill = 0)
        draw.text((414,80), 'task2', font = font18, fill = 0)
        draw.text((414,105), 'task3', font = font18, fill = 0)
        draw.text((414,130), 'task4', font = font18, fill = 0)
        draw.text((414,155), 'task5', font = font18, fill = 0)
        draw.text((414,180), 'task6', font = font18, fill = 0)
        draw.text((414,205), 'task7', font = font18, fill = 0)
        draw.text((414,230), 'task8', font = font18, fill = 0)
        draw.text((414,255), 'task9', font = font18, fill = 0)
        draw.text((414,280), 'task10', font = font18, fill = 0)
        draw.text((414,305), 'task11', font = font18, fill = 0)
        draw.text((414,330), 'task12', font = font18, fill = 0)
        draw.text((414,355), 'task13', font = font18, fill = 0)
        draw.text((414,380), 'task14', font = font18, fill = 0)
        draw.text((414,405), 'task15', font = font18, fill = 0)
        draw.text((414,430), 'task16', font = font18, fill = 0)
        
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)

    # partial update
    logging.info("5.show time")
    epd.init_part()

    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()
