from GoogleCalendar import GoogleCalendar
import os
import  datetime
import pandas as pd
import time 

cal_ids = {
    'DH 132A': 'CALENDAR_ID_HERE',
    'DH 132B': 'CALENDAR_ID_HERE',
    'DH 132D': 'CALENDAR_ID_HERE',
    'DH 132E': 'CALENDAR_ID_HERE',
    'DH 132F': 'CALENDAR_ID_HERE',
    'DH 132G': 'CALENDAR_ID_HERE',
    'DH 132H': 'CALENDAR_ID_HERE',
    'DH 132J': 'CALENDAR_ID_HERE',
    'DH 135': 'CALENDAR_ID_HERE',
    'DH 137': 'CALENDAR_ID_HERE',
    'DH 138': 'CALENDAR_ID_HERE',
    'DH 142': 'CALENDAR_ID_HERE'
} 

os.chdir(r"C:\Users\fwi_app\Desktop\Signage\Final Software") 
delay = 300
Calendar = GoogleCalendar()
Calendar.set_credentials_file_path(r"C:\Users\fwi_app\Desktop\Signage\Final Software\Credentials.json") 
Calendar.refresh_token()
Calendar.get_calendar_service()
print('-------------------------')

while True:
    Calendar.delete_all_cards_from_list_trello()
    now = datetime.datetime.now()
    now = now.strftime('%m/%d %H:%M')
    Calendar.events = pd.DataFrame()
    Calendar.get_events_from_all_calendars(cal_ids=cal_ids)
    # Calendar.process_events(required_categories=['summary', 'location', 'description', 'start', 'end'])
    Calendar.process_events(required_categories=['summary', 'location', 'start', 'end'])
    Calendar.push_to_trello()
    print(' Updated at ' + now)
    print('-------------------------')
    time.sleep(delay)
