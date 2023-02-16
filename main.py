#Author: Devesh Nath
#Creates an instance of the Google Calendar class 
#(ie makes a copy of the box that we defined in GoogleCalendar.py)
#Uses the methods defined for that class to interact with 
#Google Calendar on a higher level
from GoogleCalendar import GoogleCalendar
import sys
import os
import  datetime
import pandas as pd
import time 
import yaml

with open(os.path.join(sys.path[0], "config.yaml"), "r") as file:
             config_yaml = yaml.safe_load(file)

cal_ids = {
    'DH 132A': config_yaml['google']['DH 132A'],
    'DH 132B': config_yaml['google']['DH 132B'],
    'DH 132D': config_yaml['google']['DH 132D'],
    'DH 132E': config_yaml['google']['DH 132E'],
    'DH 132F': config_yaml['google']['DH 132F'],
    'DH 132G': config_yaml['google']['DH 132G'],
    'DH 132H': config_yaml['google']['DH 132H'],
    'DH 132J': config_yaml['google']['DH 132J'],
    'DH 135': config_yaml['google']['DH 135'],
    'DH 137': config_yaml['google']['DH 137'],
    'DH 138': config_yaml['google']['DH 138'],
    'DH 142': config_yaml['google']['DH 142']
} 
scriptpath = config_yaml['path']['directory']
os.chdir(scriptpath)
os.chdir(os.getcwd()) 
delay = 300
Calendar = GoogleCalendar()
Calendar.set_credentials_file_path(r"{0}".format(os.path.join(os.getcwd(), "Credentials.json")))
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
    Calendar.push_to_trello()
    print(' Updated at ' + now)
    print('-------------------------')
    time.sleep(delay)
