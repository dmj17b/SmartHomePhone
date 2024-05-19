import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from applib import homescreen as hs
from applib import paint as pt
import os


def main(argv=None):
    def homeScreen(event):
        paint.destroy()
        homescreen = ttk.Canvas(master=window, width=600, height=400, bg='white')
        homescreen.grid(row = 1, column = 0)

    def paintScreen(event):
        print('paintScreen')
        paint = pt.PaintCanvas(master=window)
        paint.frame.grid(row = 1, column = 0)
    

    # Create the root window
    window = ttk.Window(themename='cyborg')
    window.bind('<Escape>', lambda e: window.destroy())
    window.title('HomePhone')
    window.geometry('800x480')
    paint = pt.PaintCanvas(master=window)

    # window.attributes('-fullscreen', True)

    # Call the header widget (time, escape button):
    header = hs.HeaderWidget(master=window)
    header.frame.grid(row=0, column=0)

    homeScreen('none')
    # Menu Widget:
    menu = hs.Menu(master=window)
    menu.button_frame.grid(row=2, column=0,sticky='s')
    menu.paintbutton.bind('<Button-1>',func = paintScreen)
    menu.homebutton.bind('<Button-1>',func = homeScreen)

    

    # run
    window.mainloop()


if __name__ == "__main__":
    main()
    


