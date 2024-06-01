import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import openai
import speech_recognition as sr
from openai import AssistantEventHandler
from typing_extensions import override
import threading



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
        self.stt = stt
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

# Get time in am/pm
    def get_time_date(self):
        # Get the time and date
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%B %d, %Y")
        time_date_string = f"{current_time} on {current_date}"
        return time_date_string



# Clears the text field
    def clear_text(self):
       self.transcription_text.delete(1.0,tk.END)

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
        self.stt.start_listening_thread()
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

# Function to stop the listening thread
    def stop_button_func(self):
        self.stt.stop_listening_thread()
        self.listen_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)



# Function to call the assistant

    # Function to call the assistant
    def call_assistant(self, query):
        print("Calling assistant!")
        # self.stt.stop_listening_thread()

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
       with self.client.beta.threads.runs.stream(
            thread_id=self.openai_thread.id,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(self),
            ) as stream:
            stream.until_done()

        

       





# EventHandler class to define
# how we want to handle the events in the response stream.

 
class EventHandler(AssistantEventHandler):
    def __init__(self, asst):
        super().__init__()
        self.asst = asst

    @override
    def on_text_created(self, text) -> None:
        self.asst.transcription_text.insert(tk.END, "\n" + self.asst.asst_name + "> ", "asst_tag")

    @override
    def on_text_delta(self, delta, snapshot):
        self.asst.transcription_text.insert(tk.END, delta.value, "msg_tag")
        self.asst.transcription_text.see(tk.END)

    @override
    def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            run_id = event.data.id
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        print("Handling required action")
        tool_outputs = []
        for tool in data.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_time_date":
                current_time = self.asst.get_time_date()
                tool_outputs.append({"tool_call_id": tool.id, "output": current_time})
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        with self.asst.client.beta.threads.runs.submit_tool_outputs_stream(
            thread_id=self.current_run.thread_id,
            run_id=self.current_run.id,
            tool_outputs=tool_outputs,
            event_handler=EventHandler(self.asst),
        ) as stream:
            for text in stream.text_deltas:
                print(text, end="", flush=True)
            print()


# TouchScrollableText class to create a text widget that can be scrolled
# Helper class to create a touch scrollable text field
class TouchScrollableText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Button-1>', self.on_touch_start)
        self.bind('<B1-Motion>', self.on_touch_move)
        self.bind('<ButtonRelease-1>', self.on_touch_end)
        self._start_y = None
        self._scroll_start_y = None

    def on_touch_start(self, event):
        self._start_y = event.y
        self._scroll_start_y = self.yview()[0]

    def on_touch_move(self, event):
        if self._start_y is not None:
            delta_y = event.y - self._start_y
            new_y = self._scroll_start_y - delta_y / self.winfo_height()
            self.yview_moveto(new_y)

    def on_touch_end(self, event):
        self._start_y = None
        self._scroll_start_y = None
