import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import os


class Clock:
    # Header widget class for displaying time and GUI title
    def __init__(self, master):
        # Initialize the header widget
        self.master = master
        self.frame = ttk.Frame(master=self.master,width=800,height=50)
        # Setting up time variables:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.localTime = tk.StringVar(value=current_time)

        # Displaying the time:
        self.label = ttk.Label(master=self.frame,
                               text='Daves GUI',
                               font='calibri 28',
                               foreground='cyan',
                               textvariable=self.localTime)
        self.label.grid(row=0, column=0)
        #Call 
        self.frame.after(100, self.updateClock)
        return

    def updateClock(self):
        # Update the displayed time every second
        t = time.localtime()
        # current_time = time.strftime("%H:%M:%S", t)
        #convert time to 12 hour format:
        current_time = time.strftime("%I:%M:%S %p", t).lstrip("0")
        self.localTime.set(value=current_time)
        self.frame.after(1, self.updateClock)
        return

class Menu:
    # Menu class for creating buttons and handling button actions
    def __init__(self, master):
        # Initialize the menu
        self.master = master
        self.buttonHeight = 5
        self.buttonWidth = 9
        self.padx = 0
        self.pady = 0
        self.ipadx = 20
        self.ipady = 5

        # Create a new frame under the master
        self.button_frame = ttk.Frame(master=self.master)
        # Create the buttons:
        self.homebutton = ttk.Button(master=self.button_frame,
                         text='Home',
                         width=self.buttonWidth,
                         style='primary')
        self.homebutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.asstbutton = ttk.Button(master=self.button_frame,
                          text='Assistants',
                          width=self.buttonWidth,
                          style='secondary')
        self.asstbutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.musicbutton = ttk.Button(master=self.button_frame,
                          text='Music',
                          width=self.buttonWidth,
                          style='warning')
        self.musicbutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.smarthomebutton = ttk.Button(master=self.button_frame,
                          text='Smart Home',
                          width=self.buttonWidth,
                          style='info')
        self.smarthomebutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.destroybutton = ttk.Button(master=self.button_frame,
                        text='Apps',
                        width=self.buttonWidth,
                        style='primary')
        self.destroybutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.settings_button = ttk.Button(master=self.button_frame,
                        text='Settings',
                        width=self.buttonWidth,
                        style='primary')
        self.settings_button.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)
        return

    
class HomePage():
    def __init__(self):

        return

    def display(self):
        # Display the home page
        self.window = ttk.Window(themename='cyborg')
        self.header = HeaderWidget(master=self.window)
        self.label = ttk.Label(master=self.window, text='Home Page', font='calibri 28', foreground='cyan')
        self.label.pack(pady=5)
        self.window.mainloop()
        return