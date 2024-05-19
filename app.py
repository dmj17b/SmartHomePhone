import numpy as np
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from applib import homescreen as hs
from applib import paint as pt
import os

import matplotlib.pyplot as plt

def main(argv=None):
    # Function to switch to the home screen
    def homeScreen(event):
        paint.frame.grid_forget()
        homescreen.grid(row=1, column=0)

    # Function to switch to the paint screen
    def paintScreen(event):
        homescreen.grid_forget()
        paint.frame.grid(row=1, column=0)



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
    homescreen = ttk.Canvas(master=window, width=600, height=390, bg='white')
    homescreen.grid(row=1, column=0)

    # Call the header widget (time, escape button):
    header = hs.HeaderWidget(master=window)
    header.frame.grid(row=0, column=0, columnspan=7, sticky='ne')

    # Menu Widget:
    menu = hs.Menu(master=window)
    menu.button_frame.grid(row=3, column=0,sticky='s',columnspan=7)
    menu.button_frame.grid_anchor('w')
    menu.paintbutton.bind('<Button-1>', func=paintScreen)
    menu.homebutton.bind('<Button-1>', func=homeScreen)

    # run
    window.mainloop()


if __name__ == "__main__":
    main()
