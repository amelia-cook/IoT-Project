import requests

# Your API key here
API_KEY = 'AIzaSyCPYurU7oRoK0nYeFll2Y5sS3oGY2VLgWM'

# The ID of the public calendar (you can find this in the calendar settings)
calendar_id = 'stickynoteiot@gmail.com'  # or the calendar ID for a public calendar

# Google Calendar API endpoint
url = f'https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events'

# https://calendar.google.com/calendar/embed?src=stickynoteiot%40gmail.com&ctz=America%2FNew_York

# Parameters to specify the time range and API key
params = {
    'key': API_KEY,  # Your API key
    'timeMin': '2025-04-03T00:00:00Z',  # Start time
    'timeMax': '2025-04-05T00:00:00Z',  # End time
    'singleEvents': 'true',  # Ensures recurring events are displayed separately
    'orderBy': 'startTime',  # Sort by start time
}

# Send the GET request to the Google Calendar API
response = requests.get(url, params=params)

# Check if the response is successful
if response.status_code == 200:
    events = response.json().get('items', [])
    if events:
        for event in events:
            print(f"Event: {event['summary']} at {event['start']['dateTime']}")
    else:
        print("No events found.")
else:
    print(f"Failed to retrieve events: {response.status_code}")
