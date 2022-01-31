from cProfile import label
import tkinter as tk 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import numpy as np
import matplotlib.pyplot as plt
import statistics
import sys

values = []
serials = []
dates = []


def show_error(e, tittle_error):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = "     error: {0} \n \
    error type: {1} \n \
    in line: {2}".format(e, exc_type, exc_tb.tb_lineno)
        tk.messagebox.showerror(tittle_error, error)


def on_pick(event):
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind


    x, size = sorted(x), len(x)

    res = [x[i + 1] - x[i] for i in range(0, size) if i+1 < size]


    index = 0
    for val in values:
        if abs(y-val) < min(res) - 0.01:
            index = values.index(val)
            break
    
    print("serial: ", serials[index])
    print("date: ", dates[index])

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
        values = x_bar
        serials = s
        dates = d

        # Define list variable for groups ranges
        r = [x.max()- x.min()] 

        # Plot x-bar and R charts
        fig, axs = plt.subplots(1, figsize=(8,3.5))
        fig.canvas.callbacks.connect('pick_event', on_pick)
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


