from GoogleCalendar import GoogleCalendar
import os
import  datetime
import pandas as pd
import time 

cal_ids = {
    'DH 132A': '187f1ca7b63d2c339d2c4960b5b8bab9b91c79c8d1af34d14f1ce7df4bc4ec9a@group.calendar.google.com',
    'DH 132B': 'j5avt91ooa3od3soh7nr9ierhs@group.calendar.google.com',
    'DH 132D': 'j3qlh1jb2cd51rfi6gt8lh8s1g@group.calendar.google.com',
    'DH 132E': 'uck44cgk8dj5joevmrvaad198k@group.calendar.google.com',
    'DH 132F': '3pq91mul7uqtlrvccbhljannes@group.calendar.google.com',
    'DH 132G': 'ac53js5his3qjdjpp4d153i1cs@group.calendar.google.com',
    'DH 132H': '1j4bs75th9ucro7km124703qs0@group.calendar.google.com',
    'DH 132J': 'e04c3mg51kv8qt339vreqkvke0@group.calendar.google.com',
    'DH 135': 'n5b8clq1bnd9eoihakkiqn70gc@group.calendar.google.com',
    'DH 137': '2fcqi6srl6jbnkpqtpttmfpl2s@group.calendar.google.com',
    'DH 138': 'vl3tfk79m72voc6mkrgms0li9o@group.calendar.google.com',
    'DH 142': 'bf2cr4qe433lgsacv0vgo9m73o@group.calendar.google.com'
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
    Calendar.process_events(required_categories=['summary', 'location', 'description', 'start', 'end'])
    # Calendar.process_events(required_categories=['summary', 'location', 'start', 'end'])
    Calendar.push_to_trello()
    print(' Updated at ' + now)
    print('-------------------------')
    time.sleep(delay)
