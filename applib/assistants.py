import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import openai
import speech_recognition as sr
from openai import AssistantEventHandler
from typing_extensions import override
import threading
import datetime
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Specifically calls an assistant designed to help with scheduling
# (Her name is Donna)
class ScheduleAssistant(AssistantEventHandler):
    def __init__(self,master,stt):
        self.asst_name = "Donna"
        self.user_name = "David"
        # Read in the openai key from text file
        keyfile = open("openaikey.txt", "r")
        OPEN_AI_KEY = keyfile.read()
        keyfile.close()

        # Initialize the openai client
        self.client = openai.OpenAI(api_key=OPEN_AI_KEY)

        # Initialize the thread and assistant
        self.openai_thread = self.client.beta.threads.create()
        self.assistant_id = "asst_y2dZ6Vx8klSm0BSMZU9GeTLA"
        self.asst_response = ""
        # Initialize the calendar stuff
        self.calendar_id = 'd235ade838a883c134c4780cb0cb45c64c8ad09add4bd6607f5680df32b7593a@group.calendar.google.com'
        self.init_google_calendar()

        self.stt = stt
        self.stt_on = True
        self.stt_stopped = False
        self.master = master
        self.frame = ttk.Frame(master=self.master,width=800,height=390)
        self.frame.configure(width=800,height=390)
        self._start_y = None
        self._scroll_start_y = None


        padx = 5
        pady = 5
        ipadx = 10
        ipady= 10
        button_width = 10
        # Create the listen button:
        self.listen_button = ttk.Button(master=self.frame,
                                      width=button_width,
                                      text="Start Listening",
                                      command = self.start_button_func,
                                      style = 'primary')

        # Create the stop button:
        self.stop_button = ttk.Button(master=self.frame,
                                    width=button_width,
                                    text="Stop Listening",
                                    state=tk.DISABLED,
                                    command = self.stop_button_func,
                                    style='warning')
                                    
        #Button to clear the text:
        self.clear_button = ttk.Button(master=self.frame,
                                       width=button_width,
                                        text = "Clear",
                                        command = self.clear_text,
                                        style = 'info')
        # Place the buttons in the grid:
        self.listen_button.grid(row=0,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky='e')
        self.stop_button.grid(row=1,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky='e')
        self.clear_button.grid(row=2,column=0,ipadx=ipadx,ipady=ipady,padx=padx,pady=pady,sticky='e')

        # Shows the text transcription between user and assistant
        self.transcription_text = TouchScrollableText(master=self.frame,
                                            height=16.25,
                                            width=53,
                                            font="Helvetica 16",
                                            wrap=tk.WORD)
        self.transcription_text.tag_configure("user_tag", foreground="cyan", font=("Helvetica", 16, "bold"))
        self.transcription_text.tag_configure("asst_tag", foreground="yellow", font=("Helvetica", 16, "bold"))
        
        self.transcription_text.tag_configure("msg_tag", foreground="white", font=("Helvetica", 14))


        #Pack into the grid
        self.transcription_text.grid(row=0,column=1,rowspan=3,sticky='e')
        # Update text box any time the transcription changes
        self.stt.transcription.trace_add('write',self.update_text)




# Clears the text field
    def clear_text(self):
       self.transcription_text.delete(1.0,tk.END)

# Function to turn stt on or off
    def toggle_stt(self):
        self.stt_on = not self.stt_on

# Adds user transcription to the text field
    def update_text(self,*args):
        query = self.stt.transcription.get()
        self.transcription_text.insert(tk.END,"\n\n"+self.user_name+"> ","user_tag")
        self.transcription_text.insert(tk.END,query + "\n","msg_tag")
        self.transcription_text.see(tk.END)
        self.call_assistant(query)
        # threading.Thread(target=self.call_assistant, args=(query,)).start()

# Function to start the listening thread
    def start_button_func(self):
        self.stt_stopped = False
        self.stt.start_listening_thread()
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

# Function to stop the listening thread
    def stop_button_func(self):
        self.stt.stop_listening_thread()
        self.listen_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.stt_stopped = True

    def pause_stt_stream(self):
        self.stt.stop_listening_thread()
        self.listen_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

# Function to call the assistant
    def call_assistant(self, query):
        print("Calling assistant!")
        if self.stt_on:
            self.pause_stt_stream()

        # Sending message to assistant
        message = self.client.beta.threads.messages.create(
            thread_id=self.openai_thread.id,
            content=query,
            role="user",
        )
        # Retrieving response from assistant:
        self.response_thread = threading.Thread(target=self.stream_response)
        self.response_thread.start()
    
# Function to call event handler and stream GPT response
    def stream_response(self):
       print(self.stt_stopped)
       with self.client.beta.threads.runs.stream(
            thread_id=self.openai_thread.id,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(self),
            ) as stream:
            stream.until_done()
            if (self.stt_on and not self.stt_stopped):
                self.start_button_func()


############################# OPENAI TOOLS #####################################
# Initializes google calendar service
    def init_google_calendar(self):
        # Load the credentials from the service account key file
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            self.cred=creds
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
        self.service = build('calendar', 'v3', credentials=creds)

# Get time in am/pm
    def get_time_date(self):
        # Get the time and date
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%B %d, %Y")
        time_date_string = f"{current_time} on {current_date}"
        return time_date_string

# Fetches upcomign events from user calendar and assistant calendar
    def get_upcoming_events(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        upcoming_events = ""

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        # Gets MY upcoming events (more important)
        user_events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = user_events_result.get('items', [])
        upcoming_events += "User scheduled events:\n"
        if not events:
            print('No upcoming events found for user calendar.')
            upcoming_events += "No upcoming events found for user calendar.\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            upcoming_events += f"{start} {event['summary']}\n"

        # Gets Donna's scheduled events (sometimes wrong, dont need to follow)
        asst_events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = asst_events_result.get('items', [])
        upcoming_events += "Assistant scheduled events:\n"
        if not events:
            print('No upcoming events found on assistant created schedule for user.')
            upcoming_events += "No upcoming events found on assistant created schedule for user.\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            upcoming_events += f"{start} {event['summary']}\n"
        return upcoming_events

# Function to publish a calendar event
    def publish_calendar_event(self, summary, start_datetime, end_datetime, timezone):
        event_data = {
            'summary': summary,
            'start': {
                'dateTime': start_datetime,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': timezone,
            },
        }
        # Create the event
        event = self.service.events().insert(calendarId=self.calendar_id, body=event_data).execute()
        # Print the event ID
        print(f"Event created: {event.get('id')}")
    
# Function to delete a calendar event
    def delete_calendar_event(self, event_start_time):
        # Get the event ID by searching for the event with the start time
        page_token = None
        while True:
            events_result = self.service.events().list(calendarId=self.calendar_id, pageToken=page_token).execute()
            events = events_result.get('items', [])
            for event in events:
                if 'start' in event and event['start'].get('dateTime', '') == event_start_time:
                    self.service.events().delete(calendarId=self.calendar_id, eventId=event['id']).execute()
                    print(f"Event deleted: {event['summary']} at {event['start']['dateTime']}")
                    response = "Event deleted"
                    return response

            page_token = events_result.get('nextPageToken')
            if not page_token:
                break
        print("No matching events found to delete.")
        response = "No matching events found to delete."
        return response

        

# EventHandler class to define how we want to handle the events in the response stream. 
class EventHandler(AssistantEventHandler):
    def __init__(self, asst):
        super().__init__()
        self.asst = asst

    @override
    def on_text_created(self, text) -> None:
        self.asst.transcription_text.insert(tk.END, "\n" + self.asst.asst_name + "> ", "asst_tag")
        print("\n" + self.asst.asst_name + "> ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.asst.transcription_text.insert(tk.END, delta.value, "msg_tag")
        self.asst.transcription_text.see(tk.END)
        print(delta.value, end="", flush=True)

    @override
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    # Handles all of the inputs/outputs tool calls the GPT will make
    def handle_requires_action(self, data, run_id):
        print("Handling required action")
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            # Get time and date
            if tool.function.name == "get_time_date":
                current_time = self.asst.get_time_date()
                tool_outputs.append({"tool_call_id": tool.id, "output": current_time})
            # Get upcoming events
            elif tool.function.name == "get_upcoming_events":
                upcoming = self.asst.get_upcoming_events()
                tool_outputs.append({"tool_call_id": tool.id, "output": upcoming})
            # Publish google calendar event
            elif tool.function.name == "publish_calendar_event":                
                json_args = tool.function.arguments
                args = json.loads(json_args)
                summary = args.get("summary")
                start_datetime = args.get("start_datetime")
                end_datetime = args.get("end_datetime")
                timezone = args.get("timezone")
                self.asst.publish_calendar_event(summary, start_datetime, end_datetime, timezone)
                tool_outputs.append({"tool_call_id": tool.id, "output": "Event published"})
            # Delete google calendar event
            elif tool.function.name == "delete_calendar_event":
                json_args = tool.function.arguments
                args = json.loads(json_args)
                event_start_time = args.get("event_start_time")
                response = self.asst.delete_calendar_event(event_start_time)
                tool_outputs.append({"tool_call_id": tool.id, "output": response})
        # Submit the tool outputs
        self.submit_tool_outputs(tool_outputs, run_id)

    # Function to submit tool outputs
    def submit_tool_outputs(self, tool_outputs, run_id):
        with self.asst.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.asst),
        ) as stream:
            stream.until_done()
        


# TouchScrollableText class to create a text widget that can be scrolled
# Helper class to create a touch scrollable text field
class TouchScrollableText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.unbind('<Button-1>')
        self.unbind('<B1-Motion>')
        self.unbind('<ButtonRelease-1>')
        self.bind('<Button-1>', self.on_touch_start)
        self.bind('<B1-Motion>', self.on_touch_move)
        self.bind('<ButtonRelease-1>', self.on_touch_end)
        self._start_y = None
        self._scroll_start_y = None

    def on_touch_start(self, event):
        self._start_y = event.y
        self._scroll_start_y = self.yview()[0]
        return 'break'

    def on_touch_move(self, event):
        if self._start_y is not None:
            delta_y = event.y - self._start_y
            new_y = self._scroll_start_y - delta_y / self.winfo_height()
            self.yview_moveto(new_y)
        return 'break'

    def on_touch_end(self, event):
        self._start_y = None
        self._scroll_start_y = None
        return 'break'
