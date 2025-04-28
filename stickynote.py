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
sticky_name = []
sticky_content = []
events = []
cal_id = ""

display_on = True

font24 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 18)
font10 = ImageFont.truetype(os.path.join(libdir, 'Font.ttc'), 10)

ipAddr = str(check_output(['hostname', '-I']))
ipAddr = ipAddr.split('\'')[1].split(' ')[0]

API_KEY_PATH = '../api-key'
file = open(API_KEY_PATH, "r")
API_KEY = file.read().replace('\n', '')

# parse()
# parameters: text          string we are parsing
#             size          size of the array we want to display
#             max_length    number of characters per line
# description: parsing through the text, after max_length characters or a new
#              line character it puts the rest of the string in the next
#              element of the array
# returns: array of all of the split up input string
def parse(text, size, max_length):
  result = []

  # Split on explicit newlines first
  lines = text.split('\n')
  
  for line in lines:
    words = line.split()
    current = ""

    for word in words:
    # add each word individually
      if len(current) + len(word) + (1 if current else 0) > max_length:
      # if there is no space, go to the next line
        result.append(current)
        current = word
      else:
        current += (" " if current else "") + word

    if current:
    # if there are remaining words
      result.append(current)

  # fill the remaining space to avoid printing garbage data
  while len(result) < size:
    result.append(" ")
          
  return result

# start_calendar()
# description: this function drives what is to be displayed when the user has
#              not put in their calendar ID
def start_calendar():
  global events 
  events = []

  events.append("Enter Google Calendar Cal ID to get events :)")
  while len(events) < 16:
  # fill the remaining space to avoid printing garbage data
    events.append(" ")
  print_display()

# getCalEvent()
# description: this function gets the calendar events from the Google API and
#              formats them for printing
def getCalEvent():
  global events 
  event_string = ""
  calendar_id = cal_id
  url = f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events'
  events = []
  event_length = -1
  
  # set the length of the lines for later parsing
  if len(sticky_name) == 0:
    event_length = 90
  else:
    event_length = 45
  
  # get today and tomorrow at midnight, adjusted for timezones
  init_today = datetime.today()
  today = init_today - timedelta(hours=init_today.hour,
                                 minutes=init_today.minute,
                                 seconds=init_today.second,
                                 microseconds=init_today.microsecond)
  timezone = pytz.timezone("America/New_York")
  today = timezone.localize(today)
  tomorrow = (today + timedelta(days=1)).isoformat('T')
  today = today + timedelta(hours=init_today.hour)
  today = today.isoformat('T')
  
  params = {
    'key': API_KEY,
    'timeMin': today,
    'timeMax': tomorrow,
    'singleEvents': 'true',
    'orderBy': 'startTime',
  }
  
  response = requests.get(url, params=params)
  
  if response.status_code == 200:
  # if the response is successful
    calevents = response.json().get('items', [])
    if calevents:
    # if there are events for this dat
      for event in calevents:
      # iterate through all of the day's events
        if 'date' in event['start']:
        # if the event is an all-day event
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
      
          printstring = hour + ":" + minute + " " + ampm + " - " + end_hour
          printstring += ":" + end_minute + " " + end_ampm + " " + name + " \n "
          event_string += printstring

      events = parse(event_string, 20, event_length)
    else:
      events.append("No events today!")

  else:
    print(f"Failed to retrieve events: {response.status_code}")

# display_cal(size)
#  parameters: size         the number of lines that can be printed
# description: this function prints the calendar using the global list of events
def display_cal(size):
  global events
  today = date.today()
  date_formatted = today.strftime("%A, %B %d")
  
  while len(events) < size:
  # fill the remaining space to avoid printing garbage data
    events.append(" ")
  
  y_value = 55 + (25 * (size))
  count = 0
  
  for i in range(55, y_value, 25):
  # step from the starting value to the end
    draw.text((20,i), events[count], font = font18, fill = 0)
    count = count + 1
  
  draw.text((20, 20), date_formatted, font = font24, fill = 0)

# display_task(note_task, size, x_value, y_start)
#  parameters: note_task    the content of the note to print
#              size         the number of lines to print
#              x_value      the starting x-coordinate of each line
#              y_start      the initial y-coordinate for the output
# description: this function dynamically calculates the coordinates of each
#              line to print and prints it to the display
def display_task(note_task, size, x_value, y_start):
  y_value = y_start + (25 * (size))
  count = 0

  for i in range(y_start, y_value, 25):
  # step from the starting value to the end
    if count < size:
    # if we still have lines to print
      draw.text((x_value,i), note_task[count], font = font18, fill = 0)
      count = count + 1

# create_sticky(name, content)
#  parameters: name         the name of the target sticky
#              content      the new contents
# description: this function takes in the name of a sticky note and updates its
#              contents if the name already exists within the model or creates
#              a new note if there is space
def create_sticky(name, content):
  global sticky_name
  global sticky_content
  
  if name in sticky_name:
  # if the name exists within our model
    index = sticky_name.index(name)
    sticky_content[index] = content
  elif len(sticky_name) < 3:
  # if we have space to create new stickies
    sticky_name.append(name)
    sticky_content.append(content)

# print_display()
# description: this function is the driver for updating the display, creating
#              the skeleton of the screen, writing the data, and calling upon
#              functions to retrieve calendar data and parse output
def print_display():
  global sticky_content
  global sticky_name
  global events
  global Himage
  global draw

  try:
    # remake and clear the screen
    epd = epd7in5_V2.EPD()
    Himage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Himage)
    epd.init()
    epd.Clear()
    
    if cal_id != "":
    # if there is a calendar ID, retrieve events
      getCalEvent()
    
    epd.init_fast()
    notes_count = len(sticky_name) + 1

    if notes_count == 1:
    # print just one note (the calendar)
      # write the IP address
      draw.text((709,450), ipAddr , font = font10, fill = 0)
      
      # draw the outlining square
      draw.rectangle((10, 10, 789,469), outline = 0)
      draw.line((20,50, 779,50), fill = 0)

      display_cal(16)
    
    elif notes_count == 2:
    # print two notes (the calendar and one sticky)
      # parse the note for outputting
      note1_tasks = []
      note1_tasks = parse(sticky_content[0], 16, 45)
      
      draw.text((414, 20), sticky_name[0], font = font24, fill = 0)
      draw.text((320,450), ipAddr , font = font10, fill = 0)
      
      # draw the outlining squares
      draw.rectangle((10, 10, 394, 469), outline = 0)
      draw.rectangle((404, 10, 789,469), outline = 0)
      
      draw.line((20,50, 384, 50 ), fill = 0) 
      draw.line((414, 50, 780, 50), fill = 0)

      # calendar events - left panel
      display_cal(16)

      # sticky note tasks - right panel 
      display_task(note1_tasks, 16, 414, 55)

    elif notes_count == 3:
    # print three notes (the calendar and two stickies)
      # parse the notes for outputting
      note1_tasks = []
      note2_tasks = []
      note1_tasks = parse(sticky_content[0], 7, 45)
      note2_tasks = parse(sticky_content[1], 7, 45)
  
      draw.text((414, 20), sticky_name[0], font = font24, fill = 0)
      draw.text((414, 255), sticky_name[1], font = font24, fill = 0)
      draw.text((320,450), ipAddr , font = font10, fill = 0)
      
      # draw the outlining squares
      draw.rectangle((10, 10, 394, 469), outline = 0)
      draw.rectangle((404, 10, 789,234), outline = 0)
      draw.rectangle((404, 244, 789, 469), outline = 0)
      
      draw.line((20,50, 390, 50 ), fill = 0) 
      draw.line((414, 50, 780, 50), fill = 0)
      draw.line((414, 285, 780,285), fill = 0)

      # calendar events - left panel
      display_cal(16)

      # note 1 - top right 
      display_task(note1_tasks, 7, 414, 55)

      # note 2 - bottom right 
      display_task(note2_tasks, 7, 414, 290)
      
    elif notes_count == 4:
    # print four notes (the calendar and three stickies)
      # parse the notes for outputting
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
      
      # draw the outlining squares
      draw.rectangle((10, 10, 394, 234), outline = 0)
      draw.rectangle((10, 244, 394, 469), outline = 0)
      draw.rectangle((404, 10, 789,234), outline = 0)
      draw.rectangle((404, 244, 789, 469), outline = 0)
      
      draw.line((20,50, 384, 50 ), fill = 0)
      draw.line((20,285, 384, 284 ), fill = 0)
      draw.line((414, 50, 780, 50), fill = 0)
      draw.line((414, 285, 780,285), fill = 0)
      
      # calendar events - top left
      display_cal(7)
      
      # note 1 - bottom left 
      display_task(note3_tasks, 7, 20, 290)

      # note 2 - top right 
      display_task(note1_tasks, 7, 414, 55)

      # note 3 - bottom right
      display_task(note2_tasks, 7, 414, 290)

    epd.display(epd.getbuffer(Himage))
    epd.sleep()
          
  except IOError as e:
    print(f"Exception: {e}")
      
  except KeyboardInterrupt:
    global running
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    running = False
    # exit()

# remove_sticky_display(name)
#  parameters: name         the name of the stickynote to remove
# description: this function deletes a specific sticky note from the model, if
#              it exists
def remove_sticky_display(name):
  global sticky_name 
  global sticky_content
  
  if name in sticky_name:
  # if the name exists within our model
    index = sticky_name.index(name)
    del sticky_name[index]
    del sticky_content[index]

# get_sticky_contents(name)
#  parameters: name         the name of the stickynote to get
# description: this function retrieves the contents of a sticky note, if it
#              exists within the model
#     returns: the contents of the given sticky
def get_sticky_contents(name):
  global sticky_name 
  global sticky_content
  
  if name in sticky_name:
  # if the name exists within our model
    index = sticky_name.index(name)
    return sticky_content[index]

# receive_calID()
# description: this function serves as the API endpoint for the POST request
#              targeting /calID. Receiving a google calendar ID, the model is
#              updated to store this ID and the display is updated to reflect
#              the day's events from that calendar
#     returns: successful status code and the received data
@app.route('/calID', methods=['POST'])
@cross_origin()
def receive_calID():
    global cal_id
    data = request.json
    cal_id = data['calID']
    print_display()
    return jsonify({"status": "success", "received": data}), 200

# create_Sticky()
# description: this function serves as the API endpoint for the POST request
#              targeting /createSticky. Receiving the name and contents of a
#              stickynote, the display will either update with a new note if
#              space allows or will update the contents of an existing note
#     returns: successful status code and the retrieved content
@app.route('/createSticky', methods=['POST'])
@cross_origin()
def create_Sticky():
    data = request.json
    name = data['name']
    contents = data['content']
    create_sticky(name, contents)
    print_display()
    return jsonify({"status": "success", "received": data}), 200

# get_sticky()
# description: this function serves as the API endpoint for the GET request
#              targeting /getSticky. It retrieves the contents of the sticknote
#              of the given name, if it exists
#     returns: successful status code and the retrieved content
@app.route('/getSticky', methods=['GET'])
@cross_origin()
def get_sticky():
    name = request.args.get('name') 
    content = get_sticky_contents(name)
    return jsonify({"status": "success", "content": content}), 200

# remove_sticky()
# description: this function serves as the API endpoint for the GET request
#              targeting /removeSticky. It removes the stickynote of the given
#              name, if it exists, and updates the display
#     returns: successful status code and the removed name
@app.route('/removeSticky', methods=['GET'])
@cross_origin()
def remove_sticky():
    name = request.args.get('name')
    remove_sticky_display(name)
    print_display()
    return jsonify({"status": "success", "name": name}), 200

# display_off()
# description: this function serves as the API endpoint for the GET request
#              targeting /hide. It turns the screen off to hide the display
#     returns: successful status code
@app.route('/hide', methods=['GET'])
@cross_origin()
def display_off():
  global display_on
  display_on = False
  epd = epd7in5_V2.EPD()
  epd.init()
  epd.Clear()
  epd.sleep()
  return jsonify({"status": "success", "action": "turn display off"}), 200

# display_on()
# description: this function serves as the API endpoint for the GET request
#              targeting /show. It turns the screen back on to display the 
#              calendar and sticky notes 
#     returns: successful status code
@app.route('/show', methods=['GET'])
@cross_origin()
def display_on():
  global display_on
  display_on = True
  print_display()
  return jsonify({"status": "success", "action": "turn display on"}), 200

# clear()
# description: this function serves as the API endpoint for the GET request
#              targeting /clear. It clears the data of the sticky notes and
#              resets the screen, but preserves the calendar
#     returns: successful status code
@app.route('/clear', methods=['GET'])
@cross_origin()
def clear():
  global sticky_name
  global sticky_content
  sticky_name = []
  sticky_content = []
  print_display()
  return jsonify({"status": "success", "action": "clear display"}), 200


# periodic_update()
# description: this is the worker function for the timing thread created upon
#              startup. It periodically refreshes the display to update the
#              calendar to reflect changes over time
def periodic_update():
  global running
  while running:
  # while the program is still operating, keep updating screen
    try:
      time.sleep(60 * 60) # sleep for 60 minutes
      if display_on:
        print_display()
    except KeyboardInterrupt:
      running = False
      

# TODO
if __name__ == '__main__':
  global running
  thread = threading.Thread(target=periodic_update)
  try:
    running = True
    thread.start()
    start_calendar()
    app.run(host="0.0.0.0", port=5000)
    running = False
    thread.join()
  except Exception as e:
    print(f"Exception: {e}")
  finally:
    running = False
    epd7in5_V2.epdconfig.module_exit(cleanup=True)
    thread.join()
