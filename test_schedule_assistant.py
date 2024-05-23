import openai
import os
from openai import AssistantEventHandler
from typing_extensions import override

# Set your API key from "openaikey.txt" file 
# (You will need to create this text file. Contents should only include your key)
keyfile = open("openaikey.txt", "r")
OPEN_AI_KEY = keyfile.read()
print(OPEN_AI_KEY)

# First, we create a EventHandler class to define
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


# Create a client instance
# gets API Key from environment variable OPENAI_API_KEY
client = openai.OpenAI(api_key=OPEN_AI_KEY)
 
# Create a new thread
thread = client.beta.threads.create()

# Loop to keep the conversation going:
while True:
    # Get the user's request
    request_text = input("\nuser > ")

    # Create a new message in the thread
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        content = request_text,
        role="user",
    )
    
    # Then, we use the `stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
    
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id="asst_y2dZ6Vx8klSm0BSMZU9GeTLA",
    event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

