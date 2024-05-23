import speech_recognition as sr

recognizer = sr.Recognizer()

# Use the first available microphone
mic_index = 2
with sr.Microphone(device_index=mic_index,sample_rate=44100) as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = recognizer.listen(source,timeout=15)
try:
    print("You said: " + recognizer.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")