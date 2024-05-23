from applib import assistants as asst

# Initialize speech to text helper class:
stt = asst.STT()
stt.calibrateMic()

# Initialize scheduling assistant
scarlett = asst.ScheduleAssistant(None,stt)
while True:
    scarlett.call_assistant()
    scarlett.open_response_stream()
    input("Press Enter to continue...")