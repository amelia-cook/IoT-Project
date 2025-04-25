
import sys
import os
import json
import pytz
import requests
import time
import logging
import traceback
import threading
import datetime
from datetime import date, datetime, timedelta
from waveshare_epd import epd7in5_V2
from PIL import Image,ImageDraw,ImageFont
from subprocess import check_output
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

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

API_KEY = 'AIzaSyCPYurU7oRoK0nYeFll2Y5sS3oGY2VLgWM'


def parse(text, size, max_length):
  #parsing through the text, after max_length characters or a new line character it puts the rest of the string in the next element of the array     
  result = []

  # Split on explicit newlines first
  lines = text.split('\n')
  
  for line in lines:
    words = line.split()
    current = ""

    for word in words:
      if len(current) + len(word) + (1 if current else 0) > max_length:
        result.append(current)
        current = word
      else:
        current += (" " if current else "") + word

    if current:
      result.append(current)

  while len(result) < size:
    result.append(" ")
          
  return result

def start_calendar():
  global events 
  events = []

  events.append("Enter Google Calendar Cal ID to get events :)")
  while len(events) < 16:
    events.append(" ")
  print_display()

def getCalEvent():
  global events 
  event_string = ""
  events = []

  event_length = -1

  if len(sticky_name) == 0:
    event_length = 90
  else:
    event_length = 45

  calendar_id = cal_id
  url = f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events'
  
  init_today = datetime.today()
  today = init_today - timedelta(hours=init_today.hour, minutes=init_today.minute, seconds=init_today.second, microseconds=init_today.microsecond)
  timezone = pytz.timezone("America/New_York")
  today = timezone.localize(today)
  tomorrow = (today + timedelta(days=1)).isoformat('T')
  today = today + timedelta(hours=init_today.hour)
  today = today.isoformat('T')
  
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
    if calevents:
      for event in calevents:
        if 'date' in event['start']:
          name = event['summary']
          printstring = "ALL DAY: " + name
          events.append(printstring)
        elif 'dateTime' in event['start']:
          starttime = datetime.fromisoformat(event['start']['dateTime'])
          hour = starttime.strftime("%I")
          minute = starttime.strftime("%M")
          ampm = starttime.strftime("%p")

          endtime = datetime.fromisoformat(event['end']['dateTime'])
          end_hour = endtime.strftime("%I")
          end_minute = endtime.strftime("%M")
          end_ampm = endtime.strftime("%p")

          name = event['summary']
      
          printstring = hour + ":" + minute + " " + ampm + " - " + end_hour + ":" + end_minute + " " + end_ampm + " " + name + " \n "
          event_string += printstring

      events = parse(event_string, 20, event_length)
    else:
      events.append("No events today!")
      print("No events found.")

  else:
    print(f"Failed to retrieve events: {response.status_code}")

def display_cal(size):
  global events
  today = date.today()
  date_formatted = today.strftime("%A, %B %d")
  
  while len(events) < size:
    events.append(" ")
  
  y_value = 55 + (25 * (size))
  count = 0
  
  for i in range(55, y_value, 25):
    draw.text((20,i), events[count], font = font18, fill = 0)
    count = count + 1
  
  draw.text((20, 20), date_formatted, font = font24, fill = 0)

def display_task(note_task, size, x_value, y_start):
  y_value = y_start + (25 * (size))
  count = 0

  for i in range(y_start, y_value, 25):
    if count < size:
      draw.text((x_value,i), note_task[count], font = font18, fill = 0)
      count = count + 1

def create_sticky(name, content):
  global sticky_name
  global sticky_content
  
  if name in sticky_name:
    index = sticky_name.index(name)
    sticky_content[index] = content
  elif len(sticky_name) < 3:
    sticky_name.append(name)
    sticky_content.append(content)

def print_display():
  global sticky_content
  global sticky_name
  global events
  global epd
  global Himage
  global draw

  try:
    epd = epd7in5_V2.EPD()
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    epd.init()
    epd.Clear()
    
    if cal_id != "":
      getCalEvent()
    
    epd.init_fast()
    notes_count = len(sticky_name) + 1

    if notes_count == 1:
      draw.text((709,450), ipAddr , font = font10, fill = 0)
      
      draw.rectangle((10, 10, 789,469), outline = 0)
      draw.line((20,50, 779,50), fill = 0)

      display_cal(16)
    
    elif notes_count == 2:
      note1_tasks = []

      note1_tasks = parse(sticky_content[0], 16, 45)
      
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
      note1_tasks = []
      note2_tasks = []

      note1_tasks = parse(sticky_content[0], 7, 45)
      note2_tasks = parse(sticky_content[1], 7, 45)
  
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
      note1_tasks = []
      note2_tasks = []
      note3_tasks = []

      note1_tasks = parse(sticky_content[0], 7, 45)
      note2_tasks = parse(sticky_content[1], 7, 45)
      note3_tasks = parse(sticky_content[2], 7, 45)
      
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

    epd.display(epd.getbuffer(Himage))
    epd.sleep()
          
  except IOError as e:
    print(f"Exception: {e}")
      
  except KeyboardInterrupt:
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    exit()

def remove_sticky_display(name):
  global sticky_name 
  global sticky_content
  
  if name in sticky_name:
    index = sticky_name.index(name)
    del sticky_name[index]
    del sticky_content[index]

def get_sticky_contents(name):
  if name in sticky_name:
    index = sticky_name.index(name)
    return sticky_content[index]

def periodic_update():
  time.sleep(60 * 60) # sleep for 60 minutes
  print_display()

@app.route('/calID', methods=['POST'])
@cross_origin()
def receive_calID():
    global cal_id
    data = request.json
    cal_id = data['calID']
    print_display()
    return jsonify({"status": "success", "received": data}), 200

@app.route('/createSticky', methods=['POST'])
@cross_origin()
def receive_createSticky():
    global num_stickies
    num_stickies += 1
    data = request.json

    name = data['name']
    contents = data['content']
    create_sticky(name, contents)
    print_display()
    
    return jsonify({"status": "success", "received": data}), 200

@app.route('/getSticky', methods=['GET'])
@cross_origin()
def get_sticky():
    name = request.args.get('name') 
    content = get_sticky_contents(name)
    return jsonify({"status": "success", "content": content}), 200

@app.route('/removeSticky', methods=['GET'])
@cross_origin()
def remove_sticky():
    name = request.args.get('name')
    remove_sticky_display(name)
    print_display()
    return jsonify({"status": "success", "name": name}), 200


if __name__ == '__main__':
  thread = threading.Thread(target=periodic_update)
  try:
    thread.start()
    start_calendar()
    app.run(host="0.0.0.0", port=5000)
    thread.join()
  except Exception as e:
    print(f"Exception: {e}")
  finally:
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    thread.join()
