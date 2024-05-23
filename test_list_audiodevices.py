import speech_recognition as sr

recognizer = sr.Recognizer()

# List all microphones and their indices
print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")
