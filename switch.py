#Import the Tkinter library
from tkinter import *

win= Tk()

win.geometry("750x250")
def callback(var):
   content= var.get()
   Label(win, text=content).pack()

var = StringVar()
var.trace("w", lambda name, index,mode, var=var: callback(var))

e = Entry(win, textvariable=var)
e.pack()
win.mainloop()