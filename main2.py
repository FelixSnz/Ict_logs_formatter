

from turtle import bgcolor, width
from anytree.node.node import Node
from anytree import RenderTree
import tkinter as tk
from tkinter import tix
import sys, os
from tkcalendar import DateEntry
from datetime import datetime
import dft
import spc

import time as tm

from statistics import stdev
from numpy.core.fromnumeric import mean
import pandas as pd
import glob
import os
import re
import numpy as np
import re
import base64

from tkinter import filedialog

from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Progressbar

from concurrent import futures
from concurrent import *
import os
import subprocess

import tkinter as tk
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants

import iconb64
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

logs_path = str(" ")
import localfuncs as lf
dicts_counter = 0
amount_of_nests = 0
thread_pool_executor = futures.ThreadPoolExecutor(max_workers=5)
has_limits = True
nest_numbers = []

class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        icon = iconb64.ICON

        icondata= base64.b64decode(icon)
        # print(icon)
        ## The temp file is icon.ico
        tempFile= "icon.ico"
        iconfile= open(tempFile,"wb")
        ## Extract the icon
        iconfile.write(icondata)
        iconfile.close()
        self.root.iconbitmap(tempFile)
        ## Delete the tempfile
        os.remove(tempFile)

        
        self.preview_table = None
        root.geometry('840x520')
        root.title('Logs to excel converter')
        root.configure(background='gray94')
        self.upper_top_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.export_btn = tk.Button(self.upper_top_frame, text='Export to excel')
        self.export_btn.pack(side=tk.RIGHT)
        self.export_btn["state"] = "disabled"
        exprt_btn_hover_msg = tix.Balloon(root)
        exprt_btn_hover_msg.bind_widget(self.export_btn, 
        balloonmsg="click to start the conversion export process to excel format")

        for sub in exprt_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')

        self.opn_excel_loc = tk.Button(self.upper_top_frame, text='Open excel location')
        opnexc_btn_hover_msg = tix.Balloon(root)
        opnexc_btn_hover_msg.bind_widget(self.opn_excel_loc, 
        balloonmsg="click to open the file explorer in the path of your recent exported excel file")

        for sub in opnexc_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')

        self.can_show_fails = tk.IntVar()
        self.check_btn_showerror = tk.Checkbutton(self.upper_top_frame, text = "Show failed logs?", variable = self.can_show_fails, onvalue = 1, offvalue = 0)
        self.check_btn_showerror.pack(side=tk.RIGHT)
        check_btn_hover_msg = tix.Balloon(root)
        check_btn_hover_msg.bind_widget(self.check_btn_showerror, 
        balloonmsg="check or not before the conversion process")

        for sub in check_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')

        self.upper_top_frame.pack(fill=tk.BOTH)
        self.top_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.path_label = tk.Label(self.top_frame, text='          Logs path: ', bg='gray94')
        self.path_label.pack(side=tk.LEFT)
        self.textEntryPath = tk.StringVar()
        self.pathEntry = tk.Entry(self.top_frame, textvariable=self.textEntryPath, bg='white')
        self.pathEntry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.textEntryPath.trace("w", lambda name, index,mode, var=self.textEntryPath: self.pathEntry_callback(var))
        self.browse_btn = tk.Button(self.top_frame, text=' browse', command=lambda:self.browse_for_path())
        self.browse_btn.pack(side=tk.LEFT,  anchor=tk.NW)
        brws_btn_hover_msg = tix.Balloon(root)
        brws_btn_hover_msg.bind_widget(self.browse_btn, 
        balloonmsg="click to browse the directory of the logs")

        for sub in brws_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')
        
        self.top_frame.pack(fill=tk.BOTH)
        

        self.sec_top_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.path_label = tk.Label(self.sec_top_frame, text='Serial (optional): ', bg='gray94')
        self.path_label.pack(side=tk.LEFT)
        self.textEntrySerial = tk.StringVar()
        self.serialEntry = tk.Entry(self.sec_top_frame, textvariable=self.textEntrySerial, bg='white')
        self.serialEntry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.convert_btn = tk.Button(self.sec_top_frame, text='convert', command=lambda:thread_pool_executor.submit(self.log_to_excel_process))
        self.convert_btn.pack(side=tk.LEFT,  anchor=tk.NW)
        self.convert_btn["state"] = "disabled"
        cnvrt_btn_hover_msg = tix.Balloon(root)
        cnvrt_btn_hover_msg.bind_widget(self.convert_btn, 
        balloonmsg="click to start the conversion process")

        for sub in cnvrt_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')
        
        self.sec_top_frame.pack(fill=tk.BOTH)

        

        self.pre_top = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.pre_top_up = tk.Frame(self.root, bg='gray94', highlightthickness=2)

        self.from_label = tk.Label(self.pre_top_up, text="From:", bg='gray94')
        self.from_label.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        
        self.from_cal = DateEntry(self.pre_top_up, selectmode="day", year=2000, month=1,day=13, bg='gray94')
        self.from_cal.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.from_time_lbl = tk.Label(self.pre_top_up, text="00:00 AM", bg='gray94')
        self.from_time_lbl.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        self.from_time_btn = tk.Button(self.pre_top_up, text="Set From Time", command=lambda:self.set_time(self.from_time_lbl))

        ftime_btn_ballon = tix.Balloon(root)
        ftime_btn_ballon.bind_widget(self.from_time_btn, 
        balloonmsg="click to set the 'from time' in 12h format")

        for sub in ftime_btn_ballon.subwidgets_all():
            sub.config(bg='grey')

        self.from_time_btn.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.pre_top_up.pack(fill=tk.BOTH)

        self.pre_top_down = tk.Frame(self.root, bg='gray94', highlightthickness=2)

        self.to_label = tk.Label(self.pre_top_down, text="     To:", bg='gray94')
        self.to_label.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        
        self.to_cal = DateEntry(self.pre_top_down, selectmode="day", year=2023, month=1,day=13, bg='gray94')
        self.to_cal.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.to_time_lbl = tk.Label(self.pre_top_down, text="00:00 AM", bg='gray94')
        self.to_time_lbl.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        self.to_time_btn = tk.Button(self.pre_top_down, text="   Set To Time   ", command=lambda:self.set_time(self.to_time_lbl))

        totime_btn_ballon = tix.Balloon(root)
        totime_btn_ballon.bind_widget(self.to_time_btn, 
        balloonmsg="click to set the 'to time' in 12h format")

        for sub in totime_btn_ballon.subwidgets_all():
            sub.config(bg='grey')

        self.to_time_btn.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.pre_top_down.pack(fill=tk.BOTH)

        self.pre_top.pack(fill=tk.BOTH)
        
        self.middle_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.tab_controller = TabController(self.middle_frame)

        
        self.bottom_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.bottom_frame2 = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.pb1 = Progressbar(self.bottom_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.pb1.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.progress_bar_label = tk.Label(self.bottom_frame, text='0%', bg='gray94')
        self.progress_bar_label.pack(side=tk.LEFT, anchor=tk.SW)
        self.status_label = tk.Label(self.bottom_frame2, text=' ', bg='gray94')
        self.status_label.pack(side=tk.LEFT, anchor=tk.SW)
        self.bottom_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.bottom_frame2.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.status_label.config(text=" ", bg='gray94',  fg='black')
        self.middle_frame.pack(fill=tk.BOTH, expand=True)

    def set_time(self, label):

        top = tk.Toplevel(self.root)

        time_picker = SpinTimePickerModern(top)
        # time_picker = SpinTimePickerOld(top)
        time_picker.addAll(constants.HOURS12)  # adds hours clock, minutes and period
        time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                        hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
        time_picker.configure_seprator(bg="#404040", fg="#ffffff")
        # time_picker.addHours12()
        # time_picker.addHours24()
        # time_picker.addMinutes()

        time_picker.pack(expand=True, fill="both")

        ok_btn = tk.Button(top, text="ok", command=lambda: self.updateTime(time_picker.time(), label))
        ok_btn.pack()
    
    def updateTime(self, time, label):
        label.configure(text="{}:{} {}".format(*time))
        date_vals = str(self.from_cal.get_date()).split("-")

        time_vals = self.to_24h_format(self.from_time_lbl['text'])

        # print(date_vals)
        # print(time_vals)

        for val in time_vals:
            date_vals.append(val[:2])
        




    #this function is called whenever thetext of textPathEntry widget changes
    def pathEntry_callback(self, var):
        global logs_path
        logs_path = var.get()
        if var.get() != "":

            self.convert_btn["state"] = "normal"
        else:
            self.convert_btn["state"] = "disabled"
    


    #this function is called when browse_btn is pressed and sets expected path of the logs in the variable "logs_path"
    def browse_for_path(self):
        self.status_label.config(text=" ", bg='gray94',  fg='black')
        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            global logs_path
            logs_path = tempdir
            self.textEntryPath.set(tempdir)

    #main function for all the process that leaves ready the log data for exporting into an excel file
    def log_to_excel_process(self):
        try:
            self.tab_controller.destroy_tabs()
            self.status_label.config(text=" ", bg='gray94',  fg='black')
            if self.preview_table != None:
                self.preview_table.destroy()
                self.table_tittle.destroy()
                
            self.set_buttons_state("disabled")
            global dicts_counter
            dicts_counter = 0

            set_of_trees = {}

            counter = 0

            try:
                
                all_files = [name for name in glob.iglob(logs_path + '**/**', recursive=True) if os.path.isfile(name)]
            
                if len(all_files) == 0:
                    raise NotADirectoryError

            except Exception as err:
                self.browse_btn["state"] = "normal"
                show_error(err, "invalid path")
                raise RuntimeError

            self.pb1.config(mode="determinate")
            self.status_label.config(text="calculating amount of nests...",  fg='black')
            
            self.opn_excel_loc.forget()

            for fname in glob.iglob(logs_path + '**/**', recursive=True):
                counter += 1

                self.update_progress_bar(counter, len(all_files))

                

                if os.path.isfile(fname):

                    with open(fname) as log_f:

                        raw_data = log_f.read()

                        tree = self.log_to_tree(raw_data)

                        if tree != None:

                            file_name = log_f.name.split("\\")[-1]

                            nest_number = self.get_nest_number(file_name)
                            num_lines = sum(1 for line in open(fname))

                            if not nest_number in set_of_trees:

                                if self.can_show_fails.get():
                                    set_of_trees[nest_number] = []
                                    nest_numbers.append(nest_number)
                                else:
                                    if num_lines > 30:
                                        set_of_trees[nest_number] = []
                                        nest_numbers.append(nest_number)
            counter = 0
            self.status_label.config(text="formating log files...",  fg='black')
            global amount_of_nests
            amount_of_nests = len(set_of_trees)

            for fname in glob.iglob(logs_path + '**/**', recursive=True):

                counter += 1

                self.update_progress_bar(counter, len(all_files))

                if os.path.isfile(fname):

                    with open(fname) as log_f:
                         
                        file_name = log_f.name.split("\\")[-1]

                        nest_number = self.get_nest_number(file_name)

                        raw_data = log_f.read()

                        tree = self.log_to_tree(raw_data)

                        num_lines = sum(1 for line in open(fname))
                        if tree != None:
                            if self.can_show_fails.get():
                                set_of_trees[nest_number].append(tree)
                            else:
                                if num_lines > 30:
                                    set_of_trees[nest_number].append(tree)
                        else:
                            print("?")

            data_dict, sheet_ids = self.trees_to_excel_data(set_of_trees)
            self.set_buttons_state("normal")
            root.update_idletasks()
            self.pb1['value'] = 100
            self.progress_bar_label.config(text=str(int(100))+'% | ('+ str(dicts_counter)+"/" + str(amount_of_nests)+")")
            self.status_label.config(text="Export is enabled!",  fg='black')

            self.export_btn.config(command=lambda : self.export_caller(data_dict, sheet_ids))
        except Exception as err:
            show_error(err, "data extraction error")
        
    #returns the nest number given a log file name
    def get_nest_number(self, file_name):
        if '-' in file_name:
            nest_number = file_name.split('-')[:-1]

            if len(nest_number) > 1:
                new_nest_number = ''
                for segment in nest_number:
                    new_nest_number += segment
                
                return str(new_nest_number)
            else:
                return str(nest_number[0])
                
        else:
            return 'NA'



    #general function that covers the process of converting all the trees to excel data
    def trees_to_excel_data(self, set_of_trees):
        data_dict = {}
        #temp_tn is refering to a temporal test name, and temp_sv is refering to a temporal set of values
        try:
            for trees in set_of_trees.values():

                temp_tn, temp_sv = self.dicts_to_excel_data(self.trees_to_dicts(trees))
                if not tuple(temp_tn) in data_dict:
                    data_dict[tuple(temp_tn)] = temp_sv
                else:
                    data_dict[tuple([temp_tn, 2])] = temp_sv

        except Exception as err:
            show_error(err, "data conversion error")
        return data_dict, list(set_of_trees.keys())

    

    def dicts_to_excel_data(self, dicts):


        try:

            self.status_label.config(text='separating by nests...',  fg='black')
            global amount_of_nests
            global dicts_counter
            counter = 0

            test_names = []
            # test_limits = []

            total_iterations = len(max(get_dicts_only(dicts), key=len).keys()) * len(get_dicts_only(dicts)) * 2
            self.pb1.config(mode="determinate")
            
            for dict in get_dicts_only(dicts):

                for test_name in dict.keys():

                    counter += 1
                    left_pbs_str = ' | ('+ str(dicts_counter+1)+"/" + str(amount_of_nests)+")"

                    self.update_progress_bar(counter, total_iterations, left_pbs_str)

                    if not test_name in test_names:
                        test_names.append(test_name)

            
            # total_iterations = len(get_dicts_only(dicts)[0].keys()) * len(get_dicts_only(dicts)) + len(get_dicts_only(dicts)) *len(test_names)


                
            set_of_values = []
            sample_count = 0
            test_limits = []
            for idx, dict in enumerate(get_dicts_only(dicts)):
                sample_count += 1
                values = []
                for test_name in test_names:

                    counter +=1

                    left_pbs_str = ' | ('+ str(dicts_counter+1)+"/" + str(amount_of_nests)+")"

                    self.update_progress_bar(counter, total_iterations, left_pbs_str)

                    if not test_name in list(dict.keys()):
                        # print('NOT FOUND ------------------------')
                        values.append("NONE")
                    else:
                        # print("si hay -----------------------------")
                        values.append(dict[test_name][0])
                        test_limits.append(dict[test_name][1])
                
                serial  = get_serials_only(dicts)[idx]
                date = get_dates_only(dicts)[idx]
                # print("this is a serial: ", serial)
                values.insert(0, serial)
                values.inset(1, date)
                set_of_values.append(values)

            header_labels = []
            
            test_names.insert(0, "Test names")
            header_labels.append(tuple(test_names))
            low_limits = []
            high_limits = []
            if has_limits:
            
                low_limits = lf.get_limits(dicts)
                header_labels.append(tuple(low_limits))
                # print("ll len: ", len(low_limits))
            
                high_limits = lf.get_limits(dicts, False)
                header_labels.append(tuple(high_limits))
                # print("hl len: ", len(high_limits))

            max_values = lf.get_maxs(dicts)
            header_labels.append(tuple(max_values))
            # print("max len: ", len(max_values))
            min_values = lf.get_mins(dicts)
            header_labels.append(tuple(min_values))
            # print("min len: ", len(min_values))

            mean_values = lf.get_means(dicts)
            header_labels.append(tuple(mean_values))
            # print("mean len: ", len(mean_values))

            

            # print("vals: ", test_names)

            dicts_counter += 1


                
            self.tab_controller.create_tab("Nido: " + str(nest_numbers[dicts_counter-1]), test_names, set_of_values, test_limits)



            return tuple(header_labels), set_of_values
        except Exception as err:
            show_error(err, "excel conversion error")




    def update_progress_bar(self, actual_iteracion, total_iterations, left_bars_text = ''):

        new = (actual_iteracion * 100) / total_iterations

        self.root.update_idletasks()
        new += 0.1
        new = min([new, 100])
        self.pb1['value'] = new
        
        self.progress_bar_label.config(text=str(int(new)) + '%' + left_bars_text)




    def log_to_tree(self, raw_data:str):

        try:

            if raw_data[2:7] != 'BATCH':
                raw_data = raw_data[raw_data.find("{@BATCH"):]

            root = Node('root')

            extract_data = ""

            prev_name = ''
            blck_counter = 0
            for idx, char in enumerate(raw_data):

                if char == '{':

                    name = raw_data[idx+2:raw_data.index("|", idx)]

                    if name == 'BLOCK':
                        blck_counter += 1

                    if prev_name == 'BTEST':

                        extract_data += '\n'
                    
                    elif prev_name == 'BATCH' and name == 'BTEST':
                        pass
                    elif prev_name == 'BATCH':
                        extract_data += '\n'
                    
                    prev_name = name

                elif char == '}':
                    pass
                    
                else:
                    extract_data += char
            
            new_data_ = extract_data.split("\n\n")

            btch_count = 0

            new_data = []
            for line in new_data_:

                name = line[1:3]
                
                if 'ET' in line:
                    pass
                elif name == 'PF' or name == 'TS':
                    pass
                elif line[1:6] == 'BTEST':
                    pass
                elif line[1:5] == 'TJET':
                    pass
                elif line[1:4] == 'D-T':
                    pass
                else:

                    new_data.append(line)

            for idx, data in enumerate(new_data):

                if len(data) > 1:
                    name = data[1:data.index("|", 1)]
                    serial_ = ""
                    date_ = ""
                    if name == 'BATCH' or name == '@BATCH':

                        btch_count += 1
                        blck_count = 0

                        if name == '@BATCH':
                            name = name[1:]

                        separated_batch_data = data.split("|")

                        # print("separated data: ", separated_batch_data)

                        raw_date = separated_batch_data[7]
                        year = int("20"+raw_date[0:2])
                        month = int(raw_date[2:4])
                        day = int(raw_date[4:6])
                        hour = int(raw_date[6:8])
                        min = int(raw_date[8:10])
                        seg = int(raw_date[10:12])

                        date_ = datetime(year, month, day, hour, min, seg)

                        date_vals = str(self.from_cal.get_date()).split("-")
                        time_vals = self.to_24h_format(self.from_time_lbl['text'])
                        for val in time_vals:
                            date_vals.append(val[:2])

                        from_date = dft.to_date_format(int(date_vals[0]), int(date_vals[1]), int(date_vals[2]), int(date_vals[3]), int(date_vals[4][:2]))
                        # print("from date: ", from_date)
                        # print(date_)

                        date_vals = str(self.to_cal.get_date()).split("-")
                        time_vals = self.to_24h_format(self.to_time_lbl['text'])
                        for val in time_vals:
                            date_vals.append(val[:2])
                        to_date = dft.to_date_format(int(date_vals[0]), int(date_vals[1]), int(date_vals[2]), int(date_vals[3]), int(date_vals[4][:2]))
                        # print("from date: ", to_date)
                        # print(date_vals)

                        if not dft.is_in_date_range(from_date, date_, to_date):

                            return None


                        if len(separated_batch_data) >= 16:

                            serial_ = separated_batch_data[15] # the value with the index 15 has the serial
                        else:
                            serial_ = separated_batch_data[14]
                        
                        # print("this is the expected serial: ", self.textEntrySerial.get())
                        # print("this is the found serial: ", serial_)
                        if serial_ != self.textEntrySerial.get() and self.textEntrySerial.get() != "":
                            return None

                        temp_btch_node = Node(name + str(btch_count), parent=root, serial=serial_, date = date_)

                        #this loop passes data without mesurments and keeps foreward data with mesurements

                        # if not self.can_show_fails.get():
                        new_sub_dataset = []
                        for sub_data in new_data[idx+1:]:
                            if len(sub_data) > 1:
                                name = sub_data[1:sub_data.index("|")]
                                ind_data = sub_data.split('|')

                                if len(ind_data) > 2:
                                    if "@A" in ind_data[2]:
                                        if name.startswith("@"):
                                            sub_data = sub_data[1:]
                                        else:
                                            pass
                                        new_sub_dataset.append(sub_data)

                        new_data = new_sub_dataset

                        for sub_data in new_data:

                            if len(sub_data) > 1:
                                name = sub_data[1:sub_data.index("|")]
                                if name == 'BLOCK':

                                    blck_count += 1

                                    block_data = sub_data.split('\n')[1:]

                                    t_name = sub_data.split('\n')[0].split('|')[1]

                                    temp_blck = Node(name + str(blck_count), parent=temp_btch_node, test_name=t_name)

                                    for b_data in block_data:
        
                                        ind_data = b_data.split('|') # indidual data or separated data 
                                        
                                        new_ind_data = [] #re-process data to be separated again if necessary

                                        for d in ind_data:

                                            if 'LIM' in d:
                                                split_d = d.split("@")
                                                for sd in split_d:
                                                    new_ind_data.append(sd)
                                            else:
                                                new_ind_data.append(d)

                                        ind_data = new_ind_data

                                        if len(ind_data) > 2:

                                            # print("ind data:", ind_data)
                                            global has_limits
                                            if len(ind_data) >= 4:

                                                
                                                

                                                if 'LIM' in ind_data[3]:
                                                    # print("si tiene limites")
                                                    has_limits = True

                                                    comp_name = ind_data[0][3:] #anade el nombre del componente
                                                
                                                else:

                                                    comp_name = ind_data[0][3:] + '-' + ind_data[3] # anade el tipo especifico de componente

                                                temp_comp_node = Node(comp_name, parent=temp_blck, value=ind_data[2])

                                                limit_name = ''

                                                for d in ind_data:

                                                    if 'LIM' in d:
                                                        limit_name = d
            
                                                if not limit_name == '':
                                                    limits = ind_data[-int(limit_name[-1]):]
                                                    temp_lim_node = Node(limit_name, parent=temp_comp_node, value=limits)
                                            else:
                                                has_limits = False
                                                # print("no tiene limites")
                                                if len(ind_data) == 3:

                                                    comp_name = ind_data[0][3:] #anade el nombre del componente
                                                
                                                elif len(ind_data) == 4:
                                                    comp_name = ind_data[0][3:] + '-' + ind_data[3] # anade el tipo especifico de componente

                                                temp_comp_node = Node(comp_name, parent=temp_blck, value=ind_data[2])

                                else:
                                    pass

            # print("this is the root", RenderTree(root))

            return root
        except Exception as err:
            show_error(err, "log to tree failed")
    
    def to_24h_format(self, _12h_format):
        time_vals = _12h_format[:5].split(":")
        am_pm = _12h_format[-2:]

        if am_pm == "PM":
            time_vals[0] = str(int(time_vals[0]) +12)
        
        return time_vals


    
    def trees_to_dicts(self, trees):
        

        try:

            dicts = []

            for tree in trees:
                # print(RenderTree(tree))
                # print(tree.children)

                dict = {}
                
                for batch in tree.children:

                    
                    
                    for idx, block in enumerate(batch.children): #the block has the name of the test
                        # print("children: ", block.children)
                        if len(block.children) > 1:
                            
        
                            for comp in block.children:

                                comp_name = "-" + comp.name

                                test_name = block.test_name + comp_name

                                if len(comp.children) > 0:

                                    lims = comp.children[0].value

                                    dict[test_name] = [comp.value, lims]
                                else:
                                    # print("comp: ", comp)
                                    dict[test_name] = [comp.value]
                        else:

                            if len(block.children[0].children) > 0:

                                dict[block.test_name] = [block.children[0].value, block.children[0].children[0].value]
                            else:
                                dict[block.test_name] = [block.children[0].value]
                                # print("gola")

                    dicts.append([[batch.serial, batch.date], dict])  

            return dicts

        except Exception as err:
            show_error(err, "trees to dictionary failed")
    
    def export_caller(self, dicts_data, ids):
        thread_pool_executor.submit(self.export_to_excel, dicts_data, ids)

    
    def export_to_excel(self, data_dict, ids):
        try:

            global amount_of_nests
            self.status_label.config(text=" ", bg='gray94',  fg='black')
            self.set_buttons_state("disabled")
            self.opn_excel_loc.forget()
            counter = 0
            dfs = []

            files = [('Excel Files', '*.xlsx'), 
                ('All Files', '*.*')]

            file = asksaveasfile(filetypes = files, defaultextension = files)
            for key, value in data_dict.items():

                if key[1] == 2:
                    key = key[0]
                self.status_label.config(text="sorting the data...",  fg='black')
                df = convert_to_dataframe(value, key)
                dfs.append(df)
            
            new_dfs = []
            for idx, df in enumerate(dfs):
                
                if not df.empty:
                    new_dfs.append(df)

            self.pb1.config(mode="indeterminate")
            self.pb1.start(10)
            with pd.ExcelWriter(file.name) as writer: 
                for idx, df in enumerate(new_dfs):
                    status_text = "creating sheets..."
                    pb1_label_text = str(int(0))+'% | ('+ str(idx+1)+"/" + str(amount_of_nests)+")"
                    self.progress_bar_label.config(text=pb1_label_text)
                    self.status_label.config(text=status_text,  fg='black')
                    counter += 1
                    
                    nest_id = ids[idx]
                    if not str(nest_id) == str:
                        nest_id = str(nest_id)

                    df.to_excel(writer, sheet_name='Nido '+ nest_id )
            
            self.pb1.stop()

            self.set_buttons_state("normal")
            
            self.status_label.config(text="Done!", bg='green', fg='white')
            self.opn_excel_loc.config(command=lambda:explore(file.name))
            self.opn_excel_loc.pack(side=tk.LEFT)
            self.pb1.config(mode="determinate")
        except Exception as err:
            show_error(err, "export error")
    
    def set_buttons_state(self, state:str):
        self.export_btn["state"] = state
        self.convert_btn["state"] = state
        self.browse_btn["state"] = state

            
    

def show_error(e, tittle_error):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = "     error: {0} \n \
    error type: {1} \n \
    in line: {2}".format(e, exc_type, exc_tb.tb_lineno)
        tk.messagebox.showerror(tittle_error, error)  


class TabController:
    def __init__(self, master):
        try:


            self.notebook = tk.ttk.Notebook(master)
            self.notebook.bind('<<NotebookTabChanged>>', self.tab_changued)

            self.notebook.pack(fill=tk.BOTH, expand=True)
            self.temp_tabs = []
            self.my_trees = []
            self.my_tn_tree = None
            self.my_tn_trees = []
            self.my_tree = None
            self.master = master
            self.tab_index = 0
            self.set_of_values = None
            self.test_names = None
        except Exception as err:
            show_error(err, "tab error")

        #Frames
    

        
    
    def create_tab(self, tab_name, test_names, set_of_values, test_limits):
        try:
            self.set_of_values = set_of_values
            self.test_names = test_names
            temp_tab = tk.ttk.Frame(self.notebook)
            temp_tab.pack(fill=tk.BOTH, expand=True)
            self.temp_tabs.append(temp_tab)

            self.notebook.add(temp_tab, text=tab_name)

            tree_scroll = tk.Scrollbar(temp_tab)
            
            self.my_tn_trees.append(tk.ttk.Treeview(temp_tab, yscrollcommand=tree_scroll.set))
            self.my_tn_trees[-1].pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT)
            tree_scroll.pack(side=tk.LEFT, fill=tk.Y)
            tree_scroll.config(command=self.my_tn_trees[-1].yview)
            self.my_tn_trees[-1]["columns"] = ['Test names']
            self.my_tn_trees[-1]['show'] = 'headings'
            self.my_tn_trees[-1].column('Test names' ,anchor=tk.CENTER, width=190)
            self.my_tn_trees[-1].heading('Test names',text='Test names')

            for idx, test_name in enumerate(test_names[1:]):
                self.my_tn_trees[-1].insert(parent='',index='end',iid=idx,text='', values=test_name)

            tn_tree_ballon = tix.Balloon(root)
            tn_tree_ballon.bind_widget(self.my_tn_trees[-1], 
            balloonmsg="double click a test name to see its SPC analisis chart")

            for sub in tn_tree_ballon.subwidgets_all():
                sub.config(bg='grey')


            # print("setvals: ", set_of_values)
            self.my_tn_trees[-1].bind('<Double-1>', lambda event,
                                                            tn = test_names[1:],
                                                            sv  = set_of_values,
                                                            limits = test_limits,
                                                            :self.tree_click_event(tn, sv, limits))
            
            test_names_copy = test_names[:8].copy()
            test_names_copy.append("...")
            self.my_trees.append(tk.ttk.Treeview(temp_tab))
            self.my_trees[-1]
            self.my_trees[-1].pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT)

            self.my_trees[-1]["columns"] = test_names_copy
            self.my_trees[-1]['show'] = 'headings'


            for idx, test_name in enumerate(test_names_copy):
                self.my_trees[-1].column(test_name ,anchor=tk.CENTER, width=190)
                self.my_trees[-1].heading(test_name,text=test_name)

            
            for idx, vals in enumerate(np.array(set_of_values)[:10,:8]):
                new_vals = list(vals)
                new_vals.append("...")
                self.my_trees[-1].insert(parent='',index='end',iid=idx,text='', values=new_vals) 
            
        except Exception as err:
            show_error(err, "tab creation error")


        
    
    def tree_click_event(self, tn, sv, limits):
        set_of_vals = list(np.array(sv)[:])
        
        # print("vals : ", sv)
        try:
            item = self.my_tn_trees[self.tab_index].focus()
            # print("this is the item: ", item)
            # print("this is the item: ", item)
            if item != "":
                info = self.my_tn_trees[self.tab_index].item(item, 'values')
                test_name = info[0]
                limits = get_test_limits(tn, limits, test_name)
                test_values, serials, dates = get_test_values(tn, set_of_vals, test_name)

                spc.plot(test_values, test_name, limits, serials, dates)
        except Exception as err:
            show_error(err, "show spc error")

        

    def tab_changued(self, event):
        try:
            if len(self.temp_tabs) > 0:
                self.tab_index = self.notebook.index(self.notebook.select())
        except Exception as err:
            show_error(err, "tab error")
        

    
    def destroy_tabs(self):
        for tab in self.temp_tabs:
            tab.destroy()
        self.temp_tabs = []
        for tree in self.my_trees:
            tree.destroy()
        for tree in self.my_tn_trees:
            tree.destroy()
        self.my_trees = []
        self.my_tn_trees = []

def get_test_limits(test_names, set_of_values, limits_test_name):
    try:
        # print("this are te sv: ", set_of_values)
        test_limits = []
        limits_idx = 0

        for idx, test_name in enumerate(test_names):
            if test_name == limits_test_name:
                limits_idx = idx
                break
        

        return set_of_values[limits_idx]
    except Exception as e:
        show_error(e, "get test limits func error")
    



def get_test_values(test_names, set_of_values, values_test_name):
    values_idx = 0
    test_values = []
    serials = []
    dates = []

    for idx, test_name in enumerate(test_names):
        if test_name == values_test_name:
            values_idx = idx
            break

    for values in set_of_values:
        serials.append(values[0][0])
        dates.append(values[0][1])
        test_values.append(values[values_idx+2])
    
    return test_values, serials, dates





def get_dicts_only(dicts):
    dicts_only = []
    for d in dicts:
        dicts_only.append(d[1])
    return dicts_only

def get_serials_only(dicts):
    serials_only = []
    for d in dicts:
        serials_only.append(d[0][0])
    return serials_only

def get_dates_only(dicts):
    dates_only = []
    for d in dicts:
        dates_only.append(d[0][1])
    return dates_only


def convert_to_dataframe(data, cols):

    new_cols = []

    for col in cols:
        new_cols.append(list(col))

    df = pd.DataFrame(data, columns = new_cols)
    df.index = np.arange(1, len(df)+1)

    return df


def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])

if __name__ == "__main__":
    root = tix.Tk()
    
    main = MainApplication(root)
    root.mainloop()
    





