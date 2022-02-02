from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
import tkinter as tk

def to_24h_format(_12h_format):
        time_vals = _12h_format[:5].split(":")
        am_pm = _12h_format[-2:]

        if am_pm == "PM":
            time_vals[0] = str(int(time_vals[0]) +12)
        
        return time_vals

def updateTime(master, time, label):
    label.configure(text="{}:{} {}".format(*time))
    date_vals = str(master.from_cal.get_date()).split("-")

    time_vals = to_24h_format(label['text'])

    for val in time_vals:
        date_vals.append(val[:2])

def set_time(master, label):

    top = tk.Toplevel(master.root)

    time_picker = SpinTimePickerModern(top)
    time_picker.addAll(constants.HOURS12)  # adds hours clock, minutes and period
    time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                    hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
    time_picker.configure_seprator(bg="#404040", fg="#ffffff")
    time_picker.pack(expand=True, fill="both")

    ok_btn = tk.Button(top, text="ok", command=lambda: updateTime(master, time_picker.time(), label))
    ok_btn.pack()
    
