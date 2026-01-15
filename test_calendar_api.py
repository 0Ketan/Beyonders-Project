import requests
from datetime import datetime, timezone, timedelta

# Google Calendar configuration
CALENDAR_ID = "cee6954b0d57fcc80568fbb73b028f41eb9025730e0d27e48c2cbe2476a6be66@group.calendar.google.com"
API_KEY = "AIzaSyCtI8MeiXXVbrKiUwndC6dqpe4y7VmF5Gs"

# Get today's date range
ist = timezone(timedelta(hours=5, minutes=30))
now = datetime.now(ist)
time_min = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
time_max = now.replace(hour=23, minute=59, second=59, microsecond=0).isoformat()

# Build API request
calendar_url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"
params = {
    'key': API_KEY,
    'timeMin': time_min,
    'timeMax': time_max,
    'singleEvents': 'true',
    'orderBy': 'startTime'
}

print("Testing Google Calendar API...")
print(f"Fetching events for: {now.strftime('%Y-%m-%d')}")
print()

# Make API request
response = requests.get(calendar_url, params=params, timeout=10)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    events = data.get('items', [])
    print(f"Events found: {len(events)}")
    print()
    
    if events:
        print("Event details:")
        for i, event in enumerate(events, 1):
            title = event.get('summary', 'No title')
            start = event.get('start', {}).get('dateTime', 'No start time')
            end = event.get('end', {}).get('dateTime', 'No end time')
            print(f"{i}. {title}")
            print(f"   Start: {start}")
            print(f"   End: {end}")
            print()
    else:
        print("No events scheduled for today.")
else:
    print(f"Error: {response.text[:500]}")
