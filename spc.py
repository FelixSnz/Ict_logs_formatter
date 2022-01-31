from cProfile import label
import tkinter as tk
from turtle import bgcolor, color, width 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import numpy as np
import matplotlib.pyplot as plt
import statistics
import sys

values = []
serials = []
dates = []


class NewWindow(tk.Toplevel):
     
    def __init__(self, master = None, serial = None, date = None):
        self.serial = serial
        self.date = date
         
        super().__init__(master = master)
        self.title("New Window")
        self.geometry("500x300")
        f = tk.Frame(self, width=300, height=200)

        label = tk.Label(f, text='this is the serial: ' + str(serial))
        date_label = tk.Label(f, text='this is the date: ' + str(date))

        f.pack()
        label.pack()
        date_label.pack()


def show_error(e, tittle_error):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = "     error: {0} \n \
    error type: {1} \n \
    in line: {2}".format(e, exc_type, exc_tb.tb_lineno)
        tk.messagebox.showerror(tittle_error, error)


def on_pick(event, root):

    global values
    global serials
    global dates

    values, size = sorted(values), len(values)
    y = event.ydata
    x_ = event.xdata

    res = [values[i + 1] - values[i] for i in range(0, size) if i+1 < size]
    print("res: ", res)

    index = 0
    clicked_value = min(values, key=lambda x:abs(x-y))
    index = values.index(clicked_value)
    
    print("this is the index: ", index)
    # print("serials: ", serials)
    # print("dates: ", dates)
    print("clicked_value: ", clicked_value)
    print("y: ", y)
    print("serial: ", serials[int(round(x_))])
    print("date: ", dates[int(round(x_))])

    a = NewWindow(root, serials[int(round(x_))], dates[int(round(x_))])

    # print('Artist picked:', event.artist)
    # print ('{} vertices picked'.format(len(ind)))
    # print ('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
    # print ('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
    # print ('Data point:', x[ind[0]], y[ind[0]]) 
  
  
# plot function is created for 
# plotting the graph in 
# tkinter window
def plot(x, t_name, limits, s, d):
    try:
        low_limit = 0
        high_limit = 0

        if len(limits) == 3:
            low_limit = limits[2]
            high_limit = limits[1]
        else:
            low_limit = limits[1]
            high_limit = limits[0]




        x = np.array(x).astype(np.float)
        x_bar = x
        global values
        global serials
        global dates
        values = x_bar
        serials = s
        dates = d

        # Define list variable for groups ranges
        r = [x.max()- x.min()] 

        # Plot x-bar and R charts
        fig, axs = plt.subplots(1, figsize=(8,3.5))
        
        low_limit = np.array(low_limit).astype(float)
        high_limit = np.array(high_limit).astype(float)

        print("this are the limits: {0}, {1} and two: {2}".format(low_limit, high_limit, limits))

        # x-bar chart
        axs.plot(x_bar, linestyle='-', marker='o', color='black')
        axs.axhline((statistics.mean(x_bar)+0.577*statistics.mean(r)), color='yellow', linestyle='dashed', label="Control Limits")
        axs.axhline((statistics.mean(x_bar)-0.577*statistics.mean(r)), color='yellow', linestyle='dashed')
        axs.axhline(low_limit, color = 'orange', linestyle = 'dashed', label = 'Test Limits')
        axs.axhline(high_limit, color = 'orange', linestyle = 'dashed')
        axs.axhline((statistics.mean(x_bar)), color='blue', label='mean')
        axs.set_title(t_name + ' Chart')
        axs.set(xlabel='Samples', ylabel='Measurements')

        fig.legend(loc=7)
        fig.tight_layout()
        fig.subplots_adjust(right=0.8)   



        # Validate points out of control limits for x-bar chart
        i = 0
        control = True
        for group in x_bar:
            if group > statistics.mean(x_bar)+0.577*statistics.mean(r) or group < statistics.mean(x_bar)-0.577*statistics.mean(r):
                print('Group', i, 'out of mean control limits!')
                control = False
            i += 1
        if control == True:
            print('All points within control limits.')
            


        plt_root = tk.Tk()
        plt_root.title('SPC')
        plt_root.geometry('780x410')

        fig.canvas.callbacks.connect('button_press_event', lambda e, rot = plt_root:on_pick(e, rot))


    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                master = plt_root)  
        canvas.draw()
    
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                    plt_root)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        plt_root.mainloop()
    except Exception as e:
        show_error(e, "plot spc function error")


