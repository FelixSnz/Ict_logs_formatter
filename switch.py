#Import the tkinter library
from tkinter import *
from tkinter.tix import *

#Create an instance of tkinter frame
win = Tk()
#Set the geometry
win.geometry("400x200")

#Create a tooltip
tip= Balloon(win)

#Create a Button widget
my_button=Button(win, text= "Python", font=('Helvetica bold', 20))
my_button.pack(pady=20)

#Bind the tooltip with button
tip.bind_widget(my_button,balloonmsg="Python is an interpreted, high-level and general-purpose programming language")

win.mainloop()