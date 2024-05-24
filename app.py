import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from applib import homescreen as hs
from applib import paint as pt
import os
from applib import assistants as asst


def main(argv=None):
    # Function to switch to the home screen
    def homeScreen(event):
        paint.frame.grid_forget()
        scarlett.frame.grid_forget()
        homescreen.grid(row=1, column=0)

    # Function to switch to the paint screen
    def paintScreen(event):
        homescreen.grid_forget()
        scarlett.frame.grid_forget()
        paint.frame.grid(row=1, column=0)

    def assistant(event):
        homescreen.grid_forget()
        paint.frame.grid_forget()
        scarlett.frame.grid(row=1,column=0)

    # Create stt object:
    stt = asst.STT()
    stt.calibrateMic()


    # Create the root window
    window = ttk.Window(themename='cyborg')
    window.bind('<Escape>', lambda e: window.destroy())
    window.title('HomePhone')
    window.geometry('800x480')
    window.attributes('-fullscreen',True)
    window.resizable(False, False)

    # Create each of the main widgets
    global paint
    paint = pt.PaintCanvas(master=window)
    global homescreen
    #Initialize scheduling assistant (scarlett)
    global scarlett
    scarlett = asst.ScheduleAssistant(master=window,stt=stt)
    homescreen = ttk.Canvas(master=window, width=600, height=390, bg='white')
    homescreen.grid(row=1, column=0)



    # Call the clock widget:
    clock = hs.Clock(master=window)
    clock.frame.grid(row=0, column=0, sticky='n',columnspan=7)

    # Menu Widget:
    menu = hs.Menu(master=window)
    menu.button_frame.grid(row=3, column=0, sticky='s',columnspan=7)
    window.grid_rowconfigure(1,weight=1)
    window.grid_rowconfigure(3,weight=3)
    window.grid_columnconfigure(0,weight=1)
    menu.paintbutton.bind('<Button-1>', func=paintScreen)
    menu.homebutton.bind('<Button-1>', func=homeScreen)
    menu.asstbutton.bind('<Button-1>', func=assistant)

    # run
    window.mainloop()


if __name__ == "__main__":

    main()
