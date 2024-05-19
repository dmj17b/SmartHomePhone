from __future__ import print_function
import datetime
import os.path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    schedule = [
        {"summary": "Gym Session", "start": "2024-05-19T09:00:00-04:00", "end": "2024-05-19T09:45:00-04:00"},
        {"summary": "Shower and Get Ready", "start": "2024-05-19T09:45:00-04:00", "end": "2024-05-19T10:15:00-04:00"},
        {"summary": "Work on Smart Home Project", "start": "2024-05-19T10:30:00-04:00", "end": "2024-05-19T12:00:00-04:00"},
        {"summary": "Lunch", "start": "2024-05-19T12:00:00-04:00", "end": "2024-05-19T13:00:00-04:00"},
        {"summary": "Work on Smart Home Project", "start": "2024-05-19T13:00:00-04:00", "end": "2024-05-19T16:00:00-04:00"},
        {"summary": "Relax/Personal Time", "start": "2024-05-19T16:00:00-04:00", "end": "2024-05-19T18:00:00-04:00"},
        {"summary": "Prepare for Dinner Plans", "start": "2024-05-19T18:00:00-04:00", "end": "2024-05-19T20:00:00-04:00"},
        {"summary": "Pick Up Dinner", "start": "2024-05-19T20:00:00-04:00", "end": "2024-05-19T21:00:00-04:00"},
        {"summary": "Drive to Christi’s House", "start": "2024-05-19T21:00:00-04:00", "end": "2024-05-19T21:30:00-04:00"},
        {"summary": "Dinner with Christi", "start": "2024-05-19T21:30:00-04:00", "end": "2024-05-19T23:00:00-04:00"}
    ]

    for event in schedule:
        event_body = {
            'summary': event['summary'],
            'start': {
                'dateTime': event['start'],
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': event['end'],
                'timeZone': 'America/New_York',
            },
        }
        service.events().insert(calendarId='primary', body=event_body).execute()

if __name__ == '__main__':
    main()