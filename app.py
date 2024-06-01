import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from applib import homescreen as hs
from applib import paint as pt
import os
from applib import assistants as asst
from applib import stt as s2t
from applib import settings as stg


def main(argv=None):
    # Function to switch to the home screen
    def homeScreen(event):
        paint.frame.grid_forget()
        donna.frame.grid_forget()
        sett.frame.grid_forget()
        homescreen.grid(row=1, column=0)

    # Function to switch to the paint screen
    def paintScreen(event):
        homescreen.grid_forget()
        donna.frame.grid_forget()
        sett.frame.grid_forget()
        paint.frame.grid(row=1, column=0)

    def assistant(event):
        homescreen.grid_forget()
        paint.frame.grid_forget()
        sett.frame.grid_forget()
        donna.frame.grid(row=1,column=0)

    def settings_screen(event):
        homescreen.grid_forget()
        paint.frame.grid_forget()
        donna.frame.grid_forget()
        sett.frame.grid(row=1,column=0,sticky='w')



    # Create the root window
    window = ttk.Window(themename='cyborg')
    window.bind('<Escape>', lambda e: window.destroy())
    window.title('HomePhone')
    window.geometry('1900x1200')
    # window.attributes('-fullscreen',True)
    window.resizable(False, False)
    
    # Create stt object:
    stt = s2t.STT(master=window,mic_index=1)
    stt.calibrateMic()

    # Create each of the main widgets
    global paint
    paint = pt.PaintCanvas(master=window)

    #Initialize scheduling assistant (donna)
    global donna
    donna = asst.ScheduleAssistant(master=window,stt=stt)

    # Create the homescreen widget (placeholder):
    homescreen = ttk.Canvas(master=window, width=600, height=390, bg='white')
    homescreen.grid(row=1, column=0)

    # Create the settings widget:
    global sett
    sett = stg.Settings(master=window)


    # Call the clock widget:
    clock = hs.Clock(master=window)
    clock.frame.grid(row=0, column=0, sticky='n',columnspan=7)

    # Menu Widget:
    menu = hs.Menu(master=window)
    menu.button_frame.grid(row=3, column=0, sticky='s',columnspan=7)
    window.grid_rowconfigure(1,weight=1)
    window.grid_rowconfigure(3,weight=3)
    window.grid_columnconfigure(0,weight=1)
    menu.settings_button.bind('<Button-1>', func=settings_screen)
    menu.homebutton.bind('<Button-1>', func=homeScreen)
    menu.asstbutton.bind('<Button-1>', func=assistant)

    # run
    window.mainloop()


if __name__ == "__main__":

    main()
