import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import os

class HeaderWidget:
    # Initialization:
    def __init__(self, master):
        # Create a new frame under the master
        self.master = master
        self.frame = ttk.Frame(master = self.master)

        # Setting up time variables:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.localTime = tk.StringVar(value=current_time)

        # Displaying the time:
        self.label = ttk.Label(master = self.frame,
                    text = 'Daves GUI',
                    font = 'calibri 28',
                    foreground = 'cyan',
                    textvariable=self.localTime)
        self.label.pack(pady=5)

        # Escape button:
        self.button = tk.Button(master = self.master, text = 'ESC', command = self.master.destroy, height = 1, width=1, bg='red')
        self.button.place(anchor='ne',x=790,y=10)
        self.frame.pack()
        self.frame.after(1,self.updateClock)
        return

    def updateClock(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        self.localTime.set(value=current_time)
        self.frame.after(1,self.updateClock)
        return
    
class Menu:
    def __init__(self,master):
        self.master = master

        self.buttonHeight = 5
        self.buttonWidth = 10
        self.state = 0

        # Create a new frame under the master
        self.button_frame = ttk.Frame(master = self.master)

        # Create the buttons:
        self.button = tk.Button(master = self.button_frame, 
                                text = 'Home', 
                                command = self.button_func, 
                                height = self.buttonHeight, 
                                width=self.buttonWidth, 
                                bg='red', 
                                fg='red')
        self.button.pack(pady=20,side='left', padx=5)

        self.button = tk.Button(master = self.button_frame, 
                                text = 'Weather', 
                                command = self.button_func, 
                                height = self.buttonHeight, 
                                width=self.buttonWidth)
        
        self.button.pack(pady=20,side='left', padx=5)

        self.button = tk.Button(master = self.button_frame, 
                                text = 'Calendar', 
                                command = self.button_func, 
                                height = self.buttonHeight, 
                                width=self.buttonWidth)
        self.button.pack(pady=20,side='left', padx=5)

        self.button = tk.Button(master = self.button_frame, 
                                text = 'Phone', 
                                command = self.button_func, 
                                height = self.buttonHeight, 
                                width=self.buttonWidth)
        self.button.pack(pady=20,side='left', padx=5)

        self.button = tk.Button(master = self.button_frame,
                                 text = 'Destroy', 
                                 command = self.destroy, 
                                 height = self.buttonHeight, 
                                 width=self.buttonWidth)
        self.button.pack(pady=20,side='left', padx=5)

        self.button_frame.pack(side = 'bottom')
        return
    
    def button_func(self):
        print("Changing output")
        return
    def destroy(self):
        self.button_frame.destroy()
        return