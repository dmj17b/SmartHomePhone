import speech_recognition as sr
import threading
import tkinter as tk

# Speech to text helper class for the assistant
class STT:
    def __init__(self,master,mic_index):
        # Setting up recognizer and mic:
        self.recognizer = sr.Recognizer()
        self.mic_index = mic_index
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
        print("Stopping listening thread")  
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
                    audio = recognizer.listen(source, timeout=1.5, phrase_time_limit=10.0)
                    print("Transcribing...")
                    transcript = recognizer.recognize_google(audio)
                    self.transcription.set(value=transcript)
                    print()
                except sr.WaitTimeoutError:
                    print("Timeout error")
                    continue
                except sr.UnknownValueError:
                    print("Google Web Speech API could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Web Speech API; {e}")

