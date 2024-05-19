import numpy as np
import time
import tkinter as tk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
import os

class PaintCanvas:
    def __init__(self,master):
        self.master = master
        self.frame = ttk.Frame(master=self.master,width=800,height=390)
        self.palette_frame = ttk.Frame(master=self.frame)

        self.canvas = tk.Canvas(master=self.frame, height=390, width=650, bg='white')
        self.colorVar = tk.StringVar(value='white')
        self.color_palette()
        self.palette_frame.grid(row=1, column=0, sticky='e')
        self.canvas.grid(row = 1, column = 1)
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.colorVar.get(),outline=self.colorVar.get())

    def clear(self):
        self.canvas.delete("all")
        return
    
    def destroy(self):
        self.palette_frame.destroy()
        self.frame.destroy()
        self.canvas.destroy()
        return
    def color_palette(self):
        buttonWidth = 5
        buttonHeight = 2
        c1 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='red'),)
        c1.config(height=buttonHeight,
            width=buttonWidth,
            foreground='red',
            background='red',
            anchor='center')
        c1.grid(row=0, column=0)

        c2 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='orange'),)
        c2.config(height=buttonHeight,
            width=buttonWidth,
            foreground='orange',
            background='orange',
            anchor='center')
        c2.grid(row=1, column=0)

        c3 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='yellow'),)
        c3.config(height=buttonHeight,
            width=buttonWidth,
            foreground='yellow',
            background='yellow',
            anchor='center')
        c3.grid(row=2, column=0)

        c4 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='green'),)
        c4.config(height=buttonHeight,
            width=buttonWidth,
            foreground='green',
            background='green',
            anchor='center')
        c4.grid(row=3, column=0)

        c5 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='blue'),)
        c5.config(height=buttonHeight,
            width=buttonWidth,
            foreground='blue',
            background='blue',
            anchor='center')
        c5.grid(row=4, column=0)

        c6 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='indigo'),)
        c6.config(height=buttonHeight,
            width=buttonWidth,
            foreground='indigo',
            background='indigo',
            anchor='center')
        c6.grid(row=5, column=0)

        c7 = tk.Button(master=self.palette_frame,
            command=lambda:self.colorVar.set(value='violet'),)
        c7.config(height=buttonHeight,
            width=buttonWidth,
            foreground='violet',
            background='violet',
            anchor='center')
        c7.grid(row=6, column=0)
        clearButton = tk.Button(master=self.palette_frame,
                 text='Clear',
                 command=self.clear,
                 width=buttonWidth,
                 bg='red',
                 anchor='n')
        clearButton.grid(row=7, column=0)
