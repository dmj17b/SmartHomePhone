import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import os

class Settings:
    # Settings widget class for displaying time and GUI title
    def __init__(self, master):
        # Initialize the header widget
        self.master = master
        self.frame = ttk.Frame(master=self.master)
        self.frame.configure(width=800, height=390)
        self.menu()


    def menu(self):
        # Create the menu canvas
        self.menu = ttk.Canvas(master=self.frame, width=200, height=390)
        # Bind the menu to the touch events
        self.menu.bind("<ButtonPress-1>", self.on_touch_start)
        self.menu.bind("<B1-Motion>", self.on_touch_scroll)
        self.menu.grid_rowconfigure(0, weight=1)
        self.menu.grid_columnconfigure(0, weight=10)
        self.menu.grid_rowconfigure(1, weight=1)
        self.menu.grid_columnconfigure(1, weight=10)
        self.last_y = 0

        # Standard sizes for menu options: 
        padx = 5
        pady = 5
        ipadx = 10
        ipady= 10
        button_width = 10

        # Create the menu buttons
        b1 = ttk.Button(master=self.menu,
                        text = "General",
                        style='primary',
                        width=10)
        b1.grid(row=0, column=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady,sticky='w')

        b2 = ttk.Button(master=self.menu,
                        text = "Audio",
                        style='primary',
                        width=10)
        b2.grid(row=1, column=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

        b3 = ttk.Button(master=self.menu,
                        text = "Display",
                        style='primary',
                        width=10)
        b3.grid(row=2, column=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

        b4 = ttk.Button(master=self.menu,
                        text = "Theme",
                        style='primary',
                        width=10)
        b4.grid(row=3, column=0, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)

        # Place the menu in the grid
        self.menu.grid(row=0, column=0, sticky='w')


    def on_touch_start(self, event):
        self.last_y = event.y

    def on_touch_scroll(self, event):
        delta = self.last_y - event.y
        self.yview_scroll(int(delta), "units")
        self.last_y = event.y
        return