import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import openai
import speech_recognition as sr
from openai import AssistantEventHandler
from typing_extensions import override
import threading

class STT:
    def __init__(self,master):
        # Setting up recognizer and mic:
        self.recognizer = sr.Recognizer()
        self.mic_index = 3
        self.source = sr.Microphone(device_index=self.mic_index, sample_rate=44100, chunk_size=1024)
        self.rec_on = False
        # Tkinter string variable to hold the transcription:
        self.transcription = tk.StringVar(master=master)

    # Wrapper function to calibrate the mic
    def calibrateMic(self):
        with self.source:
            self.recognizer.adjust_for_ambient_noise(self.source)

        
    # Listening with threading:
    def start_listening_thread(self):
        print("Starting listening thread")
        self.stop_listening = False
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def stop_listening_thread(self):
        self.stop_listening = True
        self.rec_on = False

    def listen(self):
        recognizer = self.recognizer
        recognizer.pause_threshold = 1.0  # Adjust as needed
        self.rec_on = True
        with sr.Microphone() as source:
            print("Listening... Press the stop button to stop.")

            while not self.stop_listening:
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    self.transcription.set(value = recognizer.recognize_google(audio))
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    print("Google Web Speech API could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Web Speech API; {e}")




# Specifically calls an assistant designed to help with scheduling
# (Her name is Scarlett)
class ScheduleAssistant(AssistantEventHandler):
    def __init__(self,master,stt):
        self.name = "Scarlett"

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
        self.transcription_text = tk.Text(master=self.frame,
                                            height=16.25,
                                            width=53,
                                            font="Helvetica 16",
                                            wrap=tk.WORD)
        

        self.transcription_text.grid(row=0,column=1,rowspan=3,sticky='e')
        self.stt.transcription.trace_add('write',self.update_text)

    def clear_text(self):
       self.transcription_text.delete(1.0,tk.END)
    def update_text(self,*args):
        query = self.stt.transcription.get()
        self.transcription_text.insert(tk.END,"\nuser> " + query + "\n")
        self.transcription_text.see(tk.END)
        threading.Thread(target=self.call_assistant, args=(query,)).start()

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
    def call_assistant(self, query):
        print("Calling assistant!")
        # Sending message to assistant
        message = self.client.beta.threads.messages.create(
            thread_id=self.openai_thread.id,
            content=query,
            role="user",
        )
        # Running the assistant
        self.run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.openai_thread.id,
            assistant_id=self.assistant_id
        )
        # Retrieving response from assistant:
        self.response_thread = threading.Thread(target=self.stream_response)
        self.response_thread.start()


    def stream_response(self):
       with self.client.beta.threads.runs.stream(
            thread_id=self.openai_thread.id,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(self),
            ) as stream:
            stream.until_done()

        
    def display_response(self):
        self.transcription_text.insert(tk.END, "\n\n" + self.name + "> " + self.asst_response + "\n")
       





# EventHandler class to define
# how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):    
  def __init__(self,asst):
    super().__init__()
    self.asst = asst
  

  @override
  def on_text_created(self, text) -> None:
    self.asst.transcription_text.insert(tk.END,"\nassistant>")

      
  @override
  def on_text_delta(self, delta, snapshot):
    self.asst.transcription_text.insert(tk.END,delta.value)
    self.asst.transcription_text.see(tk.END)

      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
