# Author: Devesh Nath 
# edited by Alex Pho
import datetime
import pickle
import os
import re
import requests
import json
import pandas as pd
import markdownify
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleCalendar():
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.credentials_file = None
        self.service = None
        self.token = None
        self.events = pd.DataFrame()
        self.calendar_id = 'CALENDAR_ID_HERE'

    #used to set the path of the credentials file
    def set_credentials_file_path(self, path: str):
        if not isinstance(path, str):
            raise TypeError('Path should be of type string')
        if not os.path.exists(path):
            raise RuntimeError('The specified path/folder may be incorrect, try changing directories in the terminal')
        self.credentials_file = path

    #uses the credentials and scopes given to the code 
    # to initiate a conversation with Google Calendar API
    def get_calendar_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, self.SCOPES)
                    creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            self.service = build('calendar', 'v3', credentials=creds)
        except:
            raise RuntimeError('There appears to be a token error, try refreshing the token using token_refresh method')

    #Google returns time data in a very non-readable format.
    #This function makes it more readable.
    def pretty_time(self, data, num_events, dtype):
        # empty array for holding data
        proc_data = []
        for i in range(num_events):
            try:
                # gets time data from 'dateTime' in dictionary
                temp = data[dtype][i]['dateTime']
                # creates datetime object from the extracted time data
                temp = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S-07:00')
                # gets only hour and minute info from the datetime object and returns as a string
                temp = temp.strftime('%H:%M')       
            except KeyError:
                # this except clause helps to account for day long tasks
                temp = data[dtype][i]['date']  
            except:
                raise ValueError('Dataframe might be empty')
            # appending temp data 
            proc_data.append(temp)

        return proc_data

    # This gets data for all the events 
    #in a calendar by talking to Google
    def get_events(self, max_results, timeframe):
        # checks if calendar service already exists
        if self.service == None:
            self.get_calendar_service()

        # create dateTime objects which go as arguments to the next function
        now = datetime.datetime.utcnow()
        plus_timeframe = now + datetime.timedelta(hours=timeframe[0], minutes=timeframe[1], seconds=timeframe[2])
        now = now.isoformat() + 'Z' # 'Z' indicates UTC time
        plus_timeframe = plus_timeframe.isoformat() + 'Z'

        try:
            # getting an object that holds calendar data
            events_result = self.service.events().list(
                calendarId=self.calendar_id, timeMin=now,
                timeMax=plus_timeframe, maxResults=max_results,
                singleEvents=True, orderBy='startTime').execute()
            
            # converting the data in the object to DataFrame object type
            events = events_result.get('items', [])
            events = pd.DataFrame.from_dict(events)

            # concatenate if events already exist, ignore_index arg makes sure the indexes are correctly labeled
            self.events = pd.concat([self.events, events], ignore_index=True)

        except:
            raise RuntimeError('Calendar Id might be invalid, update it by using update_calendar_id method, or else you might have used the wrong google account for obtaining the token.')

    #Proceesses the data received by google 
    #and puts it into a pandas Dataframe
    def process_events(self, pretty_time = True, required_categories = ['summary', 'location', 'description', 'start', 'end']):
        #Note on required categories: If you enter location 
        #or description in the calendar, make sure to add that 
        #to required_categories or else the program will skip it.
        for i in required_categories:
            if i not in self.events.columns:
                required_categories.remove(i)

        if self.events.empty:
            print('No upcoming events found.')

        else: 
            # tends to crash the program if a field like location is left empty
            # and there is only one event in the list
            self.events = self.events[required_categories]     
            num_events_detected = self.events.shape[0]

            if pretty_time:
                self.events['start'] = self.pretty_time(self.events, num_events_detected, 'start')
                self.events['end'] = self.pretty_time(self.events, num_events_detected, 'end')

            self.events['timings'] = [self.events['start'][i] + ' -> ' + self.events['end'][i] for i in range(len(self.events))]
            try:
                # note that the Google Calendar API returns the 
                #description in HTML. We will need to convert it to Markdown later.
                self.events['desc'] = [self.events['description'][i] for i in range(len(self.events))]
                required_categories.remove('start')
                required_categories.remove('end')
                required_categories.append('timings')
                required_categories.remove('description')
                required_categories.append('desc')
            except KeyError:
                # program tends to crash if there are no descriptions within the 
                # time frame, this circumvents that by not using description
                required_categories.remove('start')
                required_categories.remove('end')
                required_categories.append('timings')

            self.events = self.events[required_categories]

    # Refreshes the token.pickle file. This 
    #is used to keep the permissions 
    #for the API up to date.
    def refresh_token(self):
        if os.path.exists("token.pickle"):
            print("token.pickle already exists, using that token.")
        else:
            print("The file does not exist, creating token.")

        try:
            self.get_calendar_service()
        except :
            raise RuntimeError('Access was denied, repeat the process and hit continue to provide access.')

    #Changes the calendar_id attribute 
    #in the Google Calendar class
    #(Basically changes an item 
    #in the Google Calendar box)
    def update_calendar_id(self, cal_id: str):
        if not isinstance(cal_id, str):
            raise TypeError('Calendar Id should be a string')
        self.calendar_id = cal_id

    #Exports the data in the pandas dataframe to an 
    #excel file in the working directory
    #---
    #alex's note: looks like we 
    #aren't using this anymore. 
    #deprecated?
    def events_to_excel(self, sheet_name: str):
        if not isinstance(sheet_name, str):
            raise TypeError('sheet_name should be a string')
        try:
            self.events.to_excel(sheet_name)
            out = sheet_name + ' was dumped to directory'
            print(out)
        except PermissionError:
            out = sheet_name + ' may already be open, try closing it before running events_to_excel method'
            raise PermissionError(out)

    #Pushes a card to trello, to a particular list
    def push_to_trello(self, list_id = '628e6a26afeb6c3cdb169476'):
        # If this function does not work, as in no card appears on trello, try getting new API key and Token.
        cal_data = self.events
        API_key = 'API_KEY_HERE'
        API_secret = 'API_SECRET_HERE'
        Token = 'TOKEN_HERE'

        url = "https://api.trello.com/1/cards"

        headers = {
            "Accept": "application/json"
        }
        
        query = {
            'idList': list_id,
            'key': API_key,
            'token': Token,
        }

        for i in range(self.events.shape[0]):
            query['name'] = ''
            query['desc'] = ''
            try:
                for j in self.events.columns[:-1]:
                    query['name'] += str(cal_data[j][i]) + ' | ' 
                    #Convert HTML to Markdown
                    query['desc'] = markdownify.markdownify(str(self.events['desc'][i]))
            except KeyError:
                for j in self.events.columns[:-1]:
                  query['name'] += str(cal_data[j][i]) + ' | ' 
                print("No descriptions found")

            response = requests.request(
                "POST",
                url,
                headers=headers,
                params=query
            )

    #gets events from all calendars 
    #and adds them to the pandas dataframe
    def get_events_from_all_calendars(self, cal_ids, max_results = 10, timeframe = [0,15,0]):
        # timeframe[0] = hours, timeframe[1] = mins, timeframe[2] = seconds
        for i in cal_ids:
            self.update_calendar_id(cal_ids[i])
            self.get_events(max_results=max_results, timeframe=timeframe)                         

    #Returns all the unique ids for each card in a given list
    def get_cards_from_list_trello(self, list_id = '628e6a26afeb6c3cdb169476'):
        API_key = 'API_KEY_HERE'
        API_secret = 'API_SECRET_HERE'
        Token = 'TOKEN_HERE'
        
        url = "https://api.trello.com/1/lists/" + list_id + "/cards"

        headers = {
            "Accept": "application/json"
        }

        query = {
            'key': API_key,
            'token': Token
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
        )

        # json.loads converts response.text (a string of json format) to a dict
        res = json.loads(response.text)
        # adds all the card ids found in the trello list to an array
        cards = [res[i]['id'] for i in range(len(res))]
        return cards

    #Deletes a card from the trello board
    def delete_card_from_list_trello(self, card_id):
        API_key = 'API_KEY_HERE'
        API_secret = 'API_SECRET_HERE'
        Token = 'TOKEN_HERE'

        url = "https://api.trello.com/1/cards/" + card_id

        query = {
            'key': API_key,
            'token': Token
        }

        response = requests.request(
        "DELETE",
        url,
        params=query
        )

    # Uses all unique card IDs to delete all cards in a list
    def delete_all_cards_from_list_trello(self, list_id = '628e6a26afeb6c3cdb169476'):
        cards = self.get_cards_from_list_trello(list_id=list_id)
        for i in cards:
            self.delete_card_from_list_trello(card_id=i)
