import numpy as np
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import os

import matplotlib.pyplot as plt

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
        self.buttonWidth = 10
        self.menuState = tk.IntVar(value=0)


        self.padx = 0
        self.pady = 0
        self.ipadx = 20
        self.ipady = 5

        # Create a new frame under the master
        self.button_frame = ttk.Frame(master=self.master)
        # Create the buttons:
        self.homebutton = ttk.Button(master=self.button_frame,
                         text='Home',
                         command=self.homepage,
                         width=self.homepage,
                         style='primary')
        self.homebutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.phonebutton = ttk.Button(master=self.button_frame,
                          text='Phone',
                          command=self.phone,
                          width=self.buttonWidth,
                          style='secondary')
        self.phonebutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.musicbutton = ttk.Button(master=self.button_frame,
                          text='Music',
                          command=self.music,
                          width=self.buttonWidth,
                          style='warning')
        self.musicbutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.smarthomebutton = ttk.Button(master=self.button_frame,
                          text='Smart Home',
                          command=self.smartHome,
                          width=self.buttonWidth,
                          style='info')
        self.smarthomebutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.destroybutton = ttk.Button(master=self.button_frame,
                        text='Apps',
                        command=self.button_frame.destroy,
                        width=self.buttonWidth,
                        style='primary')
        self.destroybutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        self.paintbutton = ttk.Button(master=self.button_frame,
                        text='Settings',
                        width=self.buttonWidth,
                        style='primary')
        self.paintbutton.pack(pady=self.pady, side='left', padx=self.padx, ipadx=self.ipadx, ipady=self.ipady)

        return

    def homepage(self):
        # Action for the "Home" button
        print("Home Screen:")
        self.menuState.set(value=0)
        return

    def phone(self):
        # Action for the "Phone" button
        print("Phone app")
        self.menuState.set(value=1)
        return

    def music(self):
        # Action for the "Music" button
        print("Music app")
        self.menuState.set(value=2)
        return

    def smartHome(self):
        # Action for the "Smart Home" button
        print("Smart home app")
        self.menuState.set(value=3)
        return

    def settings(self):
        # Action for the "settings" button
        print("Settings app")
        self.menuState.set(value=4)
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