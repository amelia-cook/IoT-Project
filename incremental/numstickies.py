#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
#from dayevents import getCalEvents

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
from datetime import date

logging.basicConfig(level=logging.DEBUG)

def parse(text, size):
    #parsing through the text, after 35 characters or a new line character it puts the rest of the string in the next element of the array     
    max_length=45
    result = []
    current = ""

    for char in text:
        current += char
        if len(current) >= max_length or char == '\n':
            result.append(current.strip())
            current = ""

    if current:
        result.append(current.strip())

    while len(result) < size:
        result.append(" ")
            
    return result

def print_display(num_stickies, name, content):
    try:
        printstring = "num stickies= " + str(num_stickies) + ", name = " + name + ", contents = " + content
        print(printstring)
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

        #todays date
        today = date.today()
        date_formatted = today.strftime("%A, %B %d")

        #sticky note names
        sticky_name = []
        sticky_content = []
        
        if name == "calID":
            print(f"hello")
        else:        
            target_index = -1

            for i in range(len(sticky_name)):
                if sticky_name[i] == name:
                    target_index = i
                    break  # optional: stop at first match

            if target_index != -1:
                sticky_content[target_index] = content
            elif num_stickies < 3:
                sticky_name.append(name)
                sticky_content.append(content)
            
        # Drawing on the Horizontal image
        logging.info("Drawing on the Horizontal image...")
        epd.init_fast()
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        notes_count = num_stickies
        
        #notes can be 35 characters for 2 panels 
        #1 panel (calendar) can be 70 characters across 
    
        if notes_count == 1:
            events = [""] * 16
        
            draw.text((20, 20), date_formatted, font = font24, fill = 0)
            draw.text((709,450), ipAddr , font = font10, fill = 0)
            draw.rectangle((10, 10, 789,469), outline = 0)
            draw.line((20,50, 779,50), fill = 0)

            draw.text((20,55), events[0], font = font18, fill = 0)
            draw.text((20,80), events[1], font = font18, fill = 0)
            draw.text((20,105), events[2], font = font18, fill = 0)
            draw.text((20,130), events[3], font = font18, fill = 0)
            draw.text((20,155), events[4], font = font18, fill = 0)
            draw.text((20,180), events[5], font = font18, fill = 0)
            draw.text((20,205), events[6], font = font18, fill = 0)
            draw.text((20,230), events[7], font = font18, fill = 0)
            draw.text((20,255), events[8], font = font18, fill = 0)
            draw.text((20,280), events[9], font = font18, fill = 0)
            draw.text((20,305), events[10], font = font18, fill = 0)
            draw.text((20,330), events[11], font = font18, fill = 0)
            draw.text((20,355), events[12], font = font18, fill = 0)
            draw.text((20,380), events[13], font = font18, fill = 0)
            draw.text((20,405), events[14], font = font18, fill = 0)
            draw.text((20,430), events[15], font = font18, fill = 0)
        
        elif notes_count == 3:
            events = [""] *	16
            note1_tasks = []
            note2_tasks = []

            note1_tasks = parse(sticky_content[0], 7)
            note2_tasks = parse(sticky_content[1], 7)
        
            draw.text((20, 20), date_formatted, font = font24, fill = 0)
            draw.text((414, 255), sticky_name[0], font = font24, fill = 0)
            draw.text((414, 20), sticky_name[1], font = font24, fill = 0)
            draw.text((320,450), ipAddr , font = font10, fill = 0)
            
            draw.rectangle((10, 10, 394, 469), outline = 0)
            draw.rectangle((404, 10, 789,234), outline = 0)
            draw.rectangle((404, 244, 789, 469), outline = 0)
            
            draw.line((20,50, 390, 50 ), fill = 0) 
            draw.line((414, 50, 780, 50), fill = 0)
            draw.line((414, 285, 780,285), fill = 0)

            #calendar events - left panel
            draw.text((20,55), events[0], font = font18, fill = 0)
            draw.text((20,80), events[1], font = font18, fill = 0)
            draw.text((20,105), events[2], font = font18, fill = 0)
            draw.text((20,130), events[3], font = font18, fill = 0)
            draw.text((20,155), events[4], font = font18, fill = 0)
            draw.text((20,180), events[5], font = font18, fill = 0)
            draw.text((20,205), events[6], font = font18, fill = 0)
            draw.text((20,230), events[7], font = font18, fill = 0)
            draw.text((20,255), events[8], font = font18, fill = 0)
            draw.text((20,280), events[9], font = font18, fill = 0)
            draw.text((20,305), events[10], font = font18, fill = 0)
            draw.text((20,330), events[11], font = font18, fill = 0)
            draw.text((20,355), events[12], font = font18, fill = 0)
            draw.text((20,380), events[13], font = font18, fill = 0)
            draw.text((20,405), events[14], font = font18, fill = 0)
            draw.text((20,430), events[15], font = font18, fill = 0)
        
            #note 1 - top right 
            draw.text((414,55), note1_tasks[0], font = font18, fill = 0)
            draw.text((414,80), note1_tasks[1], font = font18, fill = 0)
            draw.text((414,105), note1_tasks[2], font = font18, fill = 0)
            draw.text((414,130), note1_tasks[3], font = font18, fill = 0)
            draw.text((414,155), note1_tasks[4], font = font18, fill = 0)
            draw.text((414,180), note1_tasks[5], font = font18, fill = 0)
            draw.text((414,205), note1_tasks[6], font = font18, fill = 0)
            
            #note 2 - bottom right 
            draw.text((414,290), note2_tasks[0], font = font18, fill = 0)
            draw.text((414,315), note2_tasks[1], font = font18, fill = 0)
            draw.text((414,340), note2_tasks[2], font = font18, fill = 0)
            draw.text((414,365), note2_tasks[3], font = font18, fill = 0)
            draw.text((414,390), note2_tasks[4], font = font18, fill = 0)
            draw.text((414,415), note2_tasks[5], font = font18, fill = 0)
            draw.text((414,440), note2_tasks[6], font = font18, fill = 0)
    
        elif notes_count == 4:
            events = [""] * 7
            note1_tasks = []
            note2_tasks = []
            note3_tasks = []

            note1_tasks = parse(sticky_content[0], 7)
            note2_tasks = parse(sticky_content[1], 7)
            note3_tasks = parse(sticky_content[2], 7)
            
            draw.text((20, 255), sticky_name[0], font = font24, fill = 0)
            draw.text((20, 20), date_formatted, font = font24, fill = 0)
            draw.text((414, 255), sticky_name[1], font = font24, fill = 0)
            draw.text((414, 20), sticky_name[2], font = font24, fill = 0)
            draw.text((320,220), ipAddr , font = font10, fill = 0)

            draw.rectangle((10, 10, 394, 234), outline = 0)
            draw.rectangle((10, 244, 394, 469), outline = 0)
            draw.rectangle((404, 10, 789,234), outline = 0)
            draw.rectangle((404, 244, 789, 469), outline = 0)
            
            draw.line((20,50, 384, 50 ), fill = 0)
            draw.line((20,285, 384, 284 ), fill = 0)
            draw.line((414, 50, 780, 50), fill = 0)
            draw.line((414, 285, 780,285), fill = 0)
            
            #calendar events - top left
            draw.text((20,55), events[0], font = font18, fill = 0)
            draw.text((20,80), events[1], font = font18, fill = 0)
            draw.text((20,105), events[2], font = font18, fill = 0)
            draw.text((20,130), events[3], font = font18, fill = 0)
            draw.text((20,155), events[4], font = font18, fill = 0)
            draw.text((20,180), events[5], font = font18, fill = 0)
            draw.text((20,205), events[6], font = font18, fill = 0)
            
            #note 1 - bottom left 
            draw.text((20,290), note1_tasks[0], font = font18, fill = 0)
            draw.text((20,315), note1_tasks[1], font = font18, fill = 0)
            draw.text((20,340), note1_tasks[2], font = font18, fill = 0)
            draw.text((20,365), note1_tasks[3], font = font18, fill = 0)
            draw.text((20,390), note1_tasks[4], font = font18, fill = 0)
            draw.text((20,415), note1_tasks[5], font = font18, fill = 0)
            draw.text((20,440), note1_tasks[6], font = font18, fill = 0)
            
            #note 2 - top right 
            draw.text((414,55), note2_tasks[0], font = font18, fill = 0)
            draw.text((414,80), note2_tasks[1], font = font18, fill = 0)
            draw.text((414,105), note2_tasks[2], font = font18, fill = 0)
            draw.text((414,130), note2_tasks[3], font = font18, fill = 0)
            draw.text((414,155), note2_tasks[4], font = font18, fill = 0)
            draw.text((414,180), note2_tasks[5], font = font18, fill = 0)
            draw.text((414,205), note2_tasks[6], font = font18, fill = 0)

            #note 3 - bottom right
            draw.text((414,290), note3_tasks[0], font = font18, fill = 0)
            draw.text((414,315), note3_tasks[1], font = font18, fill = 0)
            draw.text((414,340), note3_tasks[2], font = font18, fill = 0)
            draw.text((414,365), note3_tasks[3], font = font18, fill = 0)
            draw.text((414,390), note3_tasks[4], font = font18, fill = 0)
            draw.text((414,415), note3_tasks[5], font = font18, fill = 0)
            draw.text((414,440), note3_tasks[6], font = font18, fill = 0)
            
        elif notes_count == 2:
            events = [""] * 16
            note1_tasks = []

            note1_tasks = parse(sticky_content[0], 16)
            
            draw.text((20, 20), date_formatted, font = font24, fill = 0)
            draw.text((414, 20), sticky_name[0], font = font24, fill = 0)
            draw.text((320,450), ipAddr , font = font10, fill = 0)
            
            draw.rectangle((10, 10, 394, 469), outline = 0)
            draw.rectangle((404, 10, 789,469), outline = 0)
            
            draw.line((20,50, 384, 50 ), fill = 0) 
            draw.line((414, 50, 780, 50), fill = 0)

            #calendar events - left panel
            draw.text((20,55), events[0], font = font18, fill = 0)
            draw.text((20,80), events[1], font = font18, fill = 0)
            draw.text((20,105), events[2], font = font18, fill = 0)
            draw.text((20,130), events[3], font = font18, fill = 0)
            draw.text((20,155), events[4], font = font18, fill = 0)
            draw.text((20,180), events[5], font = font18, fill = 0)
            draw.text((20,205), events[6], font = font18, fill = 0)
            draw.text((20,230), events[7], font = font18, fill = 0)
            draw.text((20,255), events[8], font = font18, fill = 0)
            draw.text((20,280), events[9], font = font18, fill = 0)
            draw.text((20,305), events[10], font = font18, fill = 0)
            draw.text((20,330), events[11], font = font18, fill = 0)
            draw.text((20,355), events[12], font = font18, fill = 0)
            draw.text((20,380), events[13], font = font18, fill = 0)
            draw.text((20,405), events[14], font = font18, fill = 0)
            draw.text((20,430), events[15], font = font18, fill = 0)
            
            #sticky note tasks - right panel 
            draw.text((414,55), note1_tasks[0], font = font18, fill = 0)
            draw.text((414,80), note1_tasks[1], font = font18, fill = 0)
            draw.text((414,105), note1_tasks[2], font = font18, fill = 0)
            draw.text((414,130), note1_tasks[3], font = font18, fill = 0)
            draw.text((414,155), note1_tasks[4], font = font18, fill = 0)
            draw.text((414,180), note1_tasks[5], font = font18, fill = 0)
            draw.text((414,205), note1_tasks[6], font = font18, fill = 0)
            draw.text((414,230), note1_tasks[7], font = font18, fill = 0)
            draw.text((414,255), note1_tasks[8], font = font18, fill = 0)
            draw.text((414,280), note1_tasks[9], font = font18, fill = 0)
            draw.text((414,305), note1_tasks[10], font = font18, fill = 0)
            draw.text((414,330), note1_tasks[11], font = font18, fill = 0)
            draw.text((414,355), note1_tasks[12], font = font18, fill = 0)
            draw.text((414,380), note1_tasks[13], font = font18, fill = 0)
            draw.text((414,405), note1_tasks[14], font = font18, fill = 0)
            draw.text((414,430), note1_tasks[15], font = font18, fill = 0)
            
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
