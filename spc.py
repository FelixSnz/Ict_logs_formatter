from cProfile import label
import tkinter as tk 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

import numpy as np
import matplotlib.pyplot as plt
import statistics


  
# plot function is created for 
# plotting the graph in 
# tkinter window
def plot(x, t_name):


    x = np.array(x).astype(np.float)
    x_bar = x

    # Define list variable for groups ranges
    r = [x.max()- x.min()] 

    # Plot x-bar and R charts
    fig, axs = plt.subplots(1, figsize=(8,3.5))

    # x-bar chart
    axs.plot(x_bar, linestyle='-', marker='o', color='black')
    axs.axhline((statistics.mean(x_bar)+0.577*statistics.mean(r)), color='red', linestyle='dashed', label="Control Limits")
    axs.axhline((statistics.mean(x_bar)-0.577*statistics.mean(r)), color='red', linestyle='dashed')
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
  