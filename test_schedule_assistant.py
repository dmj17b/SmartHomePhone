from applib import stt as s2t
from applib import assistants as asst
import tkinter as tk

def main():
    root = tk.Tk()
    stt = s2t.STT(master=root,mic_index=1)
    donna = asst.ScheduleAssistant(master=root,stt=stt)
    donna.toggle_stt()
    root.after(100,lambda: run_assistant(root,donna))
    root.mainloop()

def run_assistant(root,assistant):
    while True:
      query = input("\nEnter a query: ")
      root.update()
      assistant.call_assistant(query)


if __name__ == "__main__":
    main()