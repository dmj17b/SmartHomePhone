import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import openai
import speech_recognition as sr
from openai import AssistantEventHandler
from typing_extensions import override

class STT:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic_index = 2
        self.source = sr.Microphone(device_index=self.mic_index, sample_rate=44100, chunk_size=1024)
    def calibrateMic(self):
        with self.source:
            self.recognizer.adjust_for_ambient_noise(self.source)
        input("Calibration complete. Press Enter to continue...")
    def getRequest(self):
        print("Say something!")
        with self.source:
            audio = self.recognizer.listen(self.source,timeout=15)
        try:
            print("You said: " + self.recognizer.recognize_google(audio))
            return self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Error, tell user to repeat request"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Error, tell user to repeat request"


# Specifically calls an assistant designed to help with scheduling
# (Her name is Scarlett)
class ScheduleAssistant:
    def __init__(self,master,stt):
        # Read in the openai key from text file
        keyfile = open("openaikey.txt", "r")
        OPEN_AI_KEY = keyfile.read()
        keyfile.close()
        # Initialize the openai client
        self.client = openai.OpenAI(api_key=OPEN_AI_KEY)
        # Initialize the thread and assistant
        self.thread = self.client.beta.threads.create()
        self.assistant_id = "asst_y2dZ6Vx8klSm0BSMZU9GeTLA"
        self.stt = stt
        self.master = master

    def call_assistant(self):
        query = self.stt.getRequest()
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            content = query,
            role="user",
        )
    def open_response_stream(self):
        with self.client.beta.threads.runs.stream(
            thread_id=self.thread.id,
            assistant_id=self.assistant_id,
            event_handler=EventHandler(),
        ) as stream:
            stream.until_done()
        stream.close()
    def get_response(self):
       self.client.beta.threads.runs.list(thread_id=self.thread.id)
    def new_thread(self):
       self.thread.delete()
       self.thread = self.client.beta.threads.create()
    def display_app(self):
       frame = ttk.Frame(self.master)



# EventHandler class to define
# how we want to handle the events in the response stream.
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
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
