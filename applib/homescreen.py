import numpy as np
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import os

import matplotlib.pyplot as plt

class HeaderWidget:
    # Header widget class for displaying time and GUI title
    def __init__(self, master):
        # Initialize the header widget
        self.master = master
        self.frame = ttk.Frame(master=self.master)

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
        self.label.pack(pady=5)

        # Escape button:
        self.button = tk.Button(master=self.master, text='ESC', command=self.master.destroy, height=1, width=1, bg='red')
        self.button.place(anchor='ne', x=790, y=10)
        self.frame.pack()
        self.frame.after(1, self.updateClock)
        return

    def updateClock(self):
        # Update the displayed time every second
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.localTime.set(value=current_time)
        self.frame.after(1, self.updateClock)
        return

class Menu:
    # Menu class for creating buttons and handling button actions
    def __init__(self, master):
        # Initialize the menu
        self.master = master

        self.buttonHeight = 5
        self.buttonWidth = 10
        self.state = 0

        self.padx = 5
        self.pady = 5
        self.ipadx = 5
        self.ipady = 5
        self.menu_state = 0

        # Create a new frame under the master
        self.button_frame = ttk.Frame(master=self.master)

        # Create the buttons:
        self.button = ttk.Button(master=self.button_frame,
                                 text='Home',
                                 command=self.homepage,
                                 width=self.buttonWidth,
                                 style='primary')
        self.button.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.button = ttk.Button(master=self.button_frame,
                                 text='Phone',
                                 command=self.phone,
                                 width=self.buttonWidth,
                                 style='secondary')

        self.button.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.button = ttk.Button(master=self.button_frame,
                                 text='Music',
                                 command=self.music,
                                 width=self.buttonWidth,
                                 style='warning')
        self.button.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.button = ttk.Button(master=self.button_frame,
                                 text='Smart Home',
                                 command=self.smartHome,
                                 width=self.buttonWidth,
                                 style='info')
        self.button.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.button = ttk.Button(master=self.button_frame,
                                 text='Destroy',
                                 command=self.destroy,
                                 width=self.buttonWidth,
                                 style='primary')
        self.button.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.button_frame.pack(side='bottom')
        return

    def homepage(self):
        # Action for the "Home" button
        print("Changing output")
        return

    def phone(self):
        # Action for the "Phone" button
        print("Phone app")

    def weather(self):
        # Action for the "Weather" button
        print("Weather app")

    def music(self):
        # Action for the "Music" button
        print("Music app")

    def smartHome(self):
        # Action for the "Smart Home" button
        print("Smart home app")

    def destroy(self):
        # Action for the "Destroy" button
        self.button_frame.destroy()
        return
    
class HomePage():
    def __init__(self):
        self.window = ttk.Window(themename='cyborg')

        self.window.mainloop()
        return

    def display(self):
        # Display the home page
        self.header = HeaderWidget(master=self.window)
        self.label = ttk.Label(master=self.frame, text='Home Page', font='calibri 28', foreground='cyan')
        self.label.pack(pady=5)
        return