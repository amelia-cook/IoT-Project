import requests
import time
import datetime
from datetime import datetime, timedelta
import pytz

def getCalEvent(cal_id):
    # Your API key here
    API_KEY = 'AIzaSyCPYurU7oRoK0nYeFll2Y5sS3oGY2VLgWM'

    #calendar_id = cal_id
    calendar_id = 'stickynoteiot@gmail.com'
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
        events = response.json().get('items', [])
        #print(events)
        if events:
            for event in events:
                if 'date' in event['start']:
                    #have it say all day
                    start_date = event['start']['date']
                    end_date = event['end']['date']
                    name = event['summary']
                    printstring = "ALL DAY: " + name
                    print(printstring)
                elif 'dateTime' in event['start']:
                    starttime = datetime.fromisoformat(event['start']['dateTime'])
                    hour = starttime.strftime("%I")
                    minute = starttime.strftime("%M")
                    ampm = starttime.strftime("%p")
                    name = event['summary']
                
                    printstring = hour + ":" + minute + " " + ampm + " " + name
                    print(printstring)
        else:
            print("No events found.")
    else:
        print(f"Failed to retrieve events: {response.status_code}")

def main():
    getCalEvent("calid")

if __name__ == "__main__":
    main()
