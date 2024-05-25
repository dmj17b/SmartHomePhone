from applib import assistants as asst
import tkinter as tk

root = tk.Tk()
# Initialize speech to text helper class:
stt = asst.STT(root)
stt.calibrateMic()

# Initialize scheduling assistant
scarlett = asst.ScheduleAssistant(root,stt)
scarlett.frame.pack()

root.mainloop()