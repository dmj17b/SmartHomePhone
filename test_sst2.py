import threading
import tkinter as tk
import speech_recognition as sr

class SpeechToTextApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Speech to Text")
        self.stop_listening = False

        self.label = tk.Label(master, text="Press the button to start listening")
        self.label.pack()

        self.listen_button = tk.Button(master, text="Start Listening", command=self.start_listening_thread)
        self.listen_button.pack()

        self.stop_button = tk.Button(master, text="Stop Listening", command=self.stop_listening_thread, state=tk.DISABLED)
        self.stop_button.pack()

        self.transcription_text = tk.Text(master, height=10, width=50)
        self.transcription_text.pack()

    def start_listening_thread(self):
        self.stop_listening = False
        self.listen_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def stop_listening_thread(self):
        self.stop_listening = True
        self.listen_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def listen(self):
        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 1.0  # Adjust as needed

        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening... Press the stop button to stop.")

            while not self.stop_listening:
                try:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    transcription = recognizer.recognize_google(audio)
                    print("Google Web Speech API Transcription: " + transcription)
                    self.transcription_text.insert(tk.END, transcription + "\n")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    print("Google Web Speech API could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Web Speech API; {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
