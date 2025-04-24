
from flask import Flask, request, jsonify
import json
#from numstickies import print_display
from flask_cors import CORS, cross_origin

import sys
import os

import requests
import time
import datetime
from datetime import date, datetime, timedelta
import pytz
#from dayevents import getCalEvents

import logging
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
import traceback
from subprocess import check_output

#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
num_stickies = 1
sticky_name = []
sticky_content = []
events = []
cal_id = ""

font24 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 18)
font10 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 10)

ipAddr = str(check_output(['hostname', '-I']))
ipAddr = ipAddr.split('\'')[1].split(' ')[0]
logging.info("ipaddr: " + ipAddr)

API_KEY = 'AIzaSyCPYurU7oRoK0nYeFll2Y5sS3oGY2VLgWM'

def getCalEvent():
  global events 
  events = []
  # Your API key here

  calendar_id = cal_id
  url = f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events'
  
  today = datetime.today()
  tomorrow = today + timedelta(days=1)

  today = today - timedelta(hours=today.hour, minutes=today.minute, seconds=today.second, microseconds=today.microsecond)
  
  timezone = pytz.timezone("America/New_York")
  today = timezone.localize(today)
  tomorrow = today + timedelta(days=1)
  
  today = today.isoformat('T')
  tomorrow = tomorrow.isoformat('T')
  
  params = {
    'key': API_KEY,  # Your API key
    'timeMin': today,  # Start time
    'timeMax': tomorrow,  # End time
    'singleEvents': 'true',  # Ensures recurring events are displayed separately
    'orderBy': 'startTime',  # Sort by start time
  }
  
  response = requests.get(url, params=params)
  
  # Check if the response is successful
  if response.status_code == 200:
    calevents = response.json().get('items', [])
    #print(events)
    if calevents:
      for event in calevents:
        # print("event = " + str(event))
        if 'date' in event['start']:
          #have it say all day
          start_date = event['start']['date']
          end_date = event['end']['date']
          name = event['summary']
          printstring = "ALL DAY: " + name
          events.append(printstring)
          print(printstring)
        elif 'dateTime' in event['start']:
          starttime = datetime.fromisoformat(event['start']['dateTime'])
          hour = starttime.strftime("%I")
          minute = starttime.strftime("%M")
          ampm = starttime.strftime("%p")
          name = event['summary']
      
          printstring = hour + ":" + minute + " " + ampm + " " + name
          events.append(printstring)
          print(printstring)
    else:
      events.append("there are no events")
      print("No events found.")
  else:
    print(f"Failed to retrieve events: {response.status_code}")

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

def display_cal(size):
  global events
  today = date.today()
  date_formatted = today.strftime("%A, %B %d")
  
  # print("number of events in display cal = " + str(len(events)))
  while len(events) < size:
    events.append(" ")
  
  y_value = 55 + (25 * (size))
  count = 0
  
  for i in range(55, y_value, 25):
    draw.text((20,i), events[count], font = font18, fill = 0)
    count = count + 1
  
  draw.text((20, 20), date_formatted, font = font24, fill = 0)

def display_task(note_task, size, x_value, y_start):
  #note 2 = start 55, end 430, x value = 414, skip 25
  # print("number of events in display cal = " + str(len(events)))
  y_value = y_start + (25 * (size))
  count = 0
  # print(note_task)

  for i in range(y_start, y_value, 25):
    if count < size:
      # print("size = " + str(size) + ", count = " + str(count))
      draw.text((x_value,i), note_task[count], font = font18, fill = 0)
      count = count + 1

def print_display(name, content):
  global sticky_content
  global sticky_name
  global events
  global epd
  global Himage
  global draw

  try:
    # printstring = "num stickies= " + str(num_stickies) + ", name = " + name + ", contents = " + content
    # print(printstring)
    logging.info("epd7in5_V2 Demo")
    # epd = epd7in5_V2.EPD()
    epd = epd7in5_V2.EPD()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    if name == "calID":
      getCalEvent()
      # print("called get cal events")
    else:        
      target_index = -1

      # print("lenght of sticky name before comparing = " + str(len(sticky_name)))

      for i in range(len(sticky_name)):
        if sticky_name[i] == name:
          # print("sticky name found")
          target_index = i
          break  # optional: stop at first match

      if target_index != -1:
        # print("sticky name found and changing contents")
        sticky_content[target_index] = content
      elif len(sticky_name) < 3:
        # print("sticky name not found")
        sticky_name.append(name)
        sticky_content.append(content)

    # print("lenght of sticky name after comparing = " + str(len(sticky_name)))
        
    # Drawing on the Horizontal image
    logging.info("Drawing on the Horizontal image...")
    epd.init_fast()
    notes_count = len(sticky_name) + 1
    # print("notes count = " + str(notes_count))
    #notes can be 35 characters for 2 panels 
    #1 panel (calendar) can be 70 characters across 

    if notes_count == 1:
      print("in count = 1")

      draw.text((709,450), ipAddr , font = font10, fill = 0)
      
      draw.rectangle((10, 10, 789,469), outline = 0)
      draw.line((20,50, 779,50), fill = 0)

      display_cal(16)
    
    elif notes_count == 2:
      print("in count = 2")
      note1_tasks = []

      note1_tasks = parse(sticky_content[0], 16)
      
      draw.text((414, 20), sticky_name[0], font = font24, fill = 0)
      draw.text((320,450), ipAddr , font = font10, fill = 0)
      
      draw.rectangle((10, 10, 394, 469), outline = 0)
      draw.rectangle((404, 10, 789,469), outline = 0)
      
      draw.line((20,50, 384, 50 ), fill = 0) 
      draw.line((414, 50, 780, 50), fill = 0)

      #calendar events - left panel
      display_cal(16)

      #sticky note tasks - right panel 
      display_task(note1_tasks, 16, 414, 55)

    elif notes_count == 3:
      print("in count = 3")
      note1_tasks = []
      note2_tasks = []

      note1_tasks = parse(sticky_content[0], 7)
      note2_tasks = parse(sticky_content[1], 7)
  
      draw.text((414, 20), sticky_name[0], font = font24, fill = 0)
      draw.text((414, 255), sticky_name[1], font = font24, fill = 0)
      draw.text((320,450), ipAddr , font = font10, fill = 0)
      
      draw.rectangle((10, 10, 394, 469), outline = 0)
      draw.rectangle((404, 10, 789,234), outline = 0)
      draw.rectangle((404, 244, 789, 469), outline = 0)
      
      draw.line((20,50, 390, 50 ), fill = 0) 
      draw.line((414, 50, 780, 50), fill = 0)
      draw.line((414, 285, 780,285), fill = 0)

      #calendar events - left panel
      display_cal(16)

      #note 1 - top right 
      display_task(note1_tasks, 7, 414, 55)

      #note 2 - bottom right 
      display_task(note2_tasks, 7, 414, 290)
      
    elif notes_count == 4:
      print("in count = 4")
      note1_tasks = []
      note2_tasks = []
      note3_tasks = []

      note1_tasks = parse(sticky_content[0], 7)
      note2_tasks = parse(sticky_content[1], 7)
      note3_tasks = parse(sticky_content[2], 7)
      
      draw.text((20, 255), sticky_name[2], font = font24, fill = 0)
      draw.text((414, 20), sticky_name[0], font = font24, fill = 0)
      draw.text((414, 255), sticky_name[1], font = font24, fill = 0)
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
      display_cal(7)
      
      #note 1 - bottom left 
      display_task(note3_tasks, 7, 20, 290)

      #note 2 - top right 
      display_task(note1_tasks, 7, 414, 55)

      #note 3 - bottom right
      display_task(note2_tasks, 7, 414, 290)
      
    print("finished drawing !!!!!")

    epd.display(epd.getbuffer(Himage))
    #time.sleep(2)
    
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

def get_sticky_contents(name):
  index = sticky_name.index(name)
  return sticky_content[index]

@app.route("/")
def home():
    return 'Hello from Raspberry Pi 5!'

@app.route('/calID', methods=['POST'])
@cross_origin()
def receive_calID():
    global cal_id
    data = request.json

    cal_id = data['calID']
    #getCalEvent()
    print_display("calID", cal_id)
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data}), 200

#@app.route('/createSticky', methods=['OPTIONS'])
#def createSticky_options():
#    response = jsonify(message="options allowed")
#    response.headers.add("Access-Control-Allow-Options", "*")
#    return response

@app.route('/createSticky', methods=['POST'])
@cross_origin()
def receive_createSticky():
    global num_stickies
    num_stickies += 1
    print("num stickies in recieve_createSticky= " + str(num_stickies))
    data = request.json
#    print(f"Received: {data}")

    name = data['name']
    contents = data['content']

#    print(f"about to print display")
    print_display(name, contents)
#    print(f"after print display")
    
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data}), 200

@app.route('/getSticky', methods=['GET'])
@cross_origin()
def send_sticky():
    name = request.args.get('name') 
    content = get_sticky_contents(name)
    print(f"Received: {name}")
    print(f"Sending: {content}")
    return jsonify({"status": "success", "content": content}), 200

app.run(host="0.0.0.0", port=5000)



'''
To do:
-- fix parse so that it breaks on a space
-- remove a sticky
-- code refactoring 
-- default cal print 
'''
