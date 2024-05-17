import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from applib import homescreen as hs
import os



def main(argv=None):


    # Create the root window
    window = ttk.Window(themename='cyborg')
    window.title('HomePhone')
    window.geometry('800x480')
    # window.attributes('-fullscreen', True)

    # Call the header widget (time, escape button):
    header = hs.HeaderWidget(master=window)

    # Menu Widget:
    hs.Menu(master=window)



    # run 
    window.mainloop()


if __name__ == "__main__":
    main()
    


