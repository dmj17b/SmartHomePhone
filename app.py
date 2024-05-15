import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from applib import homescreen as hs
import os



def main(argv=None):

    def button_func():
        print("Changing output")

    def updateClock():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        localTime.set(value=current_time)
        window.after(1,updateClock)

    # create a window
    window = ttk.Window(themename='cyborg')
    window.title('HomePhone')
    window.geometry('800x480')
    window.attributes('-fullscreen', True)
    



    # Time Widget:
    time_widget = ttk.Frame(master = window)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    localTime = tk.StringVar(value=current_time)

    # Call the header widget:
    header = hs.HeaderWidget(master=window)


    # Button frame:
    buttonHeight = 5
    buttonWidth = 10
    button_frame = ttk.Frame(master = window)
    button = tk.Button(master = button_frame, text = 'Home', command = button_func, height = buttonHeight, width=buttonWidth, bg='red', fg='red')
    button.pack(pady=20,side='left', padx=5)

    button = tk.Button(master = button_frame, text = 'Weather', command = button_func, height = buttonHeight, width=buttonWidth)
    button.pack(pady=20,side='left', padx=5)

    button = tk.Button(master = button_frame, text = 'Calendar', command = button_func, height = buttonHeight, width=buttonWidth)
    button.pack(pady=20,side='left', padx=5)

    button = tk.Button(master = button_frame, text = 'Phone', command = button_func, height = buttonHeight, width=buttonWidth)
    button.pack(pady=20,side='left', padx=5)

    button = tk.Button(master = button_frame, text = 'Calendar', command = button_func, height = buttonHeight, width=buttonWidth)
    button.pack(pady=20,side='left', padx=5)

    button = tk.Button(master = button_frame, text = 'Phone', command = button_func, height = buttonHeight, width=buttonWidth)
    button.pack(pady=20,side='left', padx=5)

    button_frame.pack(side = 'bottom')



    # run 
    window.after(1,updateClock)
    window.mainloop()


if __name__ == "__main__":
    main()
    


