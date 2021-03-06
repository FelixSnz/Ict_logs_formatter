from tkinter import messagebox
from anytree.node.node import Node
from anytree import RenderTree
from tkinter import tix
import sys, os
from tkcalendar import DateEntry
from datetime import datetime
from collections import defaultdict
import pandas as pd
import glob
import numpy as np
import base64
from selenium import webdriver

from tkinter.filedialog import asksaveasfile, askdirectory
from tkinter.ttk import Progressbar

from concurrent import futures


import tkinter as tk


import iconb64


logs_path = str(" ")

# ----------------- Local modules -----------------

import localfuncs as lf
import tooltip
import dft
import spc
import timepicker
import serialreport

# ------------------- END --------------------------


dicts_counter = 0
amount_of_nests = 0
thread_pool_executor = futures.ThreadPoolExecutor(max_workers=5)
has_limits = True
nest_numbers = []
failed_tests = []

units = {
    "JUM":"?",
    "RES":'Ω',
    "CAP":'F',
    "DIO":'?',
    "IND":'H'
}

# M:/Public/Luis Dominguez/64002696_p/GR&R/1

class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        icon = iconb64.ICON

        icondata= base64.b64decode(icon)

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
        


        # ------------- check button filters --------------------------
        self.can_show_empties = tk.IntVar()
        self.check_btn_showempties = tk.Checkbutton(self.upper_top_frame, text = "Show empty logs?", variable = self.can_show_empties, onvalue = 1, offvalue = 0)
        self.check_btn_showempties.pack(side=tk.RIGHT)

        tooltip.CreateToolTip(self.check_btn_showempties, "check or not before the conversion process")

        self.can_show_dups = tk.IntVar()
        self.check_btn_showdups = tk.Checkbutton(self.upper_top_frame, text = "Show duplicate serials?", variable = self.can_show_dups, onvalue = 1, offvalue = 0)
        self.check_btn_showdups.pack(side=tk.RIGHT)

        tooltip.CreateToolTip(self.check_btn_showdups, "check or not before the conversion process")

        self.can_show_fails = tk.IntVar()
        self.check_btn_showfails = tk.Checkbutton(self.upper_top_frame, text = "Show failed tests?", variable = self.can_show_fails, onvalue = 1, offvalue = 0)
        self.check_btn_showfails.pack(side=tk.RIGHT)

        tooltip.CreateToolTip(self.check_btn_showfails, "check or not before the conversion process")

        # ----------------------- END ---------------------------------
        

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

        tooltip.CreateToolTip(self.browse_btn, "click to browse the directory of the logs")

        
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

        tooltip.CreateToolTip(self.convert_btn, "click to start the conversion process")
        
        self.sec_top_frame.pack(fill=tk.BOTH)

        

        self.pre_top = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.pre_top_up = tk.Frame(self.root, bg='gray94', highlightthickness=2)

        self.from_label = tk.Label(self.pre_top_up, text="From:", bg='gray94')
        self.from_label.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        
        self.from_cal = DateEntry(self.pre_top_up, selectmode="day", year=2000, month=1,day=13, bg='gray94')
        self.from_cal.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.from_time_lbl = tk.Label(self.pre_top_up, text="00:00 AM", bg='gray94')
        self.from_time_lbl.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        self.from_time_btn = tk.Button(self.pre_top_up, text="Set From Time", command=lambda:timepicker.set_time(self, self.from_time_lbl))

        tooltip.CreateToolTip(self.from_time_btn, "click to set the 'from time' in 12h format")

        self.from_time_btn.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.pre_top_up.pack(fill=tk.BOTH)

        self.pre_top_down = tk.Frame(self.root, bg='gray94', highlightthickness=2)

        self.to_label = tk.Label(self.pre_top_down, text="     To:", bg='gray94')
        self.to_label.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        
        self.to_cal = DateEntry(self.pre_top_down, selectmode="day", year=2023, month=1,day=13, bg='gray94')
        self.to_cal.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.to_time_lbl = tk.Label(self.pre_top_down, text="00:00 AM", bg='gray94')
        self.to_time_lbl.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        self.to_time_btn = tk.Button(self.pre_top_down, text="   Set To Time   ", command=lambda:timepicker.set_time(self, self.to_time_lbl))

        tooltip.CreateToolTip(self.to_time_btn, "click to set the 'to time' in 12h format")

        self.to_time_btn.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)
        self.pre_top_down.pack(fill=tk.BOTH)

        self.pre_top.pack(fill=tk.BOTH)
        
        self.middle_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.tab_controller = TabController(self.middle_frame)

        
        self.bottom_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        
        self.bottom_frame2 = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.export_btn = tk.Button(self.bottom_frame2, text='Export to excel')
        self.export_btn.pack(side=tk.RIGHT)
        self.export_btn["state"] = "disabled"

        tooltip.CreateToolTip(self.export_btn, "click to start the conversion export process to excel format")

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
        tempdir = askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            global logs_path
            logs_path = tempdir
            self.textEntryPath.set(tempdir)

    #main function for all the process that leaves ready the log data for exporting into an excel file
    def log_to_excel_process(self):
        try:
            print("about to destroy tabs")
            global nest_numbers
            nest_numbers = []
            self.tab_controller.destroy_tabs()
            self.status_label.config(text=" ", bg='gray94',  fg='black')
            if self.preview_table != None:
                self.preview_table.destroy()
                self.table_tittle.destroy()
                
            self.set_buttons_state("disabled")
            global dicts_counter
            dicts_counter = 0

            set_of_trees = defaultdict(list)

            counter = 0
            
            try:
                
                all_files = [name for name in glob.iglob(logs_path + '/**', recursive=True) if os.path.isfile(name)]
            
                if len(all_files) == 0:
                    raise NotADirectoryError

            except Exception as err:
                self.browse_btn["state"] = "normal"
                show_error(err, "invalid path")
                raise RuntimeError
            
            

            counter = 0
            self.status_label.config(text="formating log files...",  fg='black')
            for fname in glob.iglob(logs_path + '/**', recursive=True):

                counter += 1

                self.update_progress_bar(counter, len(all_files))

                if os.path.isfile(fname):

                    with open(fname) as log_f:
                         
                        file_name = log_f.name.split("\\")[-1]

                        nest_number = self.get_nest_number(file_name)
                        
                        if not nest_number in nest_numbers:
                            nest_numbers.append(nest_number)

                        raw_data = log_f.read()

                        tree = self.log_to_tree(raw_data)

                        num_lines = sum(1 for line in open(fname))
                        if tree != None:
                            if self.can_show_empties.get():
                                if self.can_show_dups.get():
                                    set_of_trees[nest_number].append(tree)
                                elif not self.has_serial(set_of_trees[nest_number], tree):
                                    set_of_trees[nest_number].append(tree)
                            elif num_lines > 35:
                                if self.can_show_dups.get():
                                    set_of_trees[nest_number].append(tree)
                                elif not self.has_serial(set_of_trees[nest_number], tree):
                                    set_of_trees[nest_number].append(tree)
                        else:
                            print("empty/none tree")
            global amount_of_nests
            amount_of_nests = len(set_of_trees)
            # print("set of trees: ", set_of_trees)
            data_dict, sheet_ids = self.trees_to_excel_data(set_of_trees)
            self.set_buttons_state("normal")
            self.root.update_idletasks()
            self.pb1['value'] = 100
            self.progress_bar_label.config(text=str(int(100))+'% | ('+ str(dicts_counter)+"/" + str(amount_of_nests)+")")
            
            # print("dd: ", data_dict)
            
            if data_dict != {}:
                self.status_label.config(text="Export is enabled!",  fg='black')
                if messagebox.askokcancel(message="el formato a sido completado \n¿Desea exportar ahora?", title='Formateo completo'):
                    self.export_caller(data_dict, sheet_ids)
            else:
                messagebox.showwarning(message="There were no matches for the inserted date or serial", title="Logs not found")
                self.status_label.config(text="No matched logs",  fg='black')
                self.export_btn["state"] = "disabled"


            self.export_btn.config(command=lambda : self.export_caller(data_dict, sheet_ids))
        except Exception as err:
            show_error(err, "data extraction error")

    
    def has_serial(self, trees, tree):
        try:
            for master_tree in trees:
                for master_batch in master_tree.children:
                    for batch in tree.children:
                        if master_batch.serial == batch.serial:
                            return True
            return False
        except Exception as e:
            show_error(e, "duplicate check error")

        
    #returns the nest number given a log file name
    def get_nest_number(self, file_name):
        if '-' in file_name:
            nest_number = file_name.split('-')[:-1]
            if len(nest_number) < 4:
                return nest_number[0]
            else:
                return 'NA'
                
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

            total_iterations = len(max(lf.get_dicts_only(dicts), key=len).keys()) * len(lf.get_dicts_only(dicts)) * 2
            self.pb1.config(mode="determinate")
            
            for dict in lf.get_dicts_only(dicts):

                for test_name in dict.keys():

                    counter += 1
                    left_pbs_str = ' | ('+ str(dicts_counter+1)+"/" + str(amount_of_nests)+")"

                    self.update_progress_bar(counter, total_iterations, left_pbs_str)

                    if not test_name in test_names:
                        test_names.append(test_name)

        
            set_of_values = []
            sample_count = 0
            test_limits = []
            for idx, dict in enumerate(lf.get_dicts_only(dicts)):
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
                
                serial  = lf.get_serials_only(dicts)[idx]
                date = lf.get_dates_only(dicts)[idx]
                # print("this is a serial: ", serial)
                values.insert(0, serial)
                values.insert(1, date)
                set_of_values.append(values)
                
            test_names.insert(0, "")
            test_names.insert(0, "Test names")
            # print("test names result: ", test_names)
            
            err_index = len(test_names)

            # if not self.can_show_fails.get():

            #     err_idxs = []
                
            #     for values in set_of_values:

            #         values = list(values)
                    
            #         if not values.count("NONE") == len(values) - 2:
            #             if "NONE" in values:
            #                 err_idxs.append(values.index("NONE"))
                
            #     if len(err_idxs) > 0:
                
            #         err_index = min(err_idxs)
            #         new_set_of_values = []
            #         for values in set_of_values:
            #             new_set_of_values.append(values[:err_index])
            #             # print("len of new vals: ", len(values[:err_index]))
                    
            #         set_of_values = new_set_of_values
            #         test_names = test_names[:err_index]
            #         # print("len of new tests_names: ", len(test_names))
            
            # for values in set_of_values:
            #     print("vals len: ", len(values))
            # print("tn len: ", len(test_names))
                 
            header_labels = []

            header_labels.append(tuple(test_names))

            # print("hd labels: ", header_labels)
            low_limits = []
            high_limits = []
            if has_limits:
            
                low_limits = lf.get_limits(dicts)
                low_limits.insert(1, "")
                header_labels.append(tuple(low_limits[:err_index]))
            
                high_limits = lf.get_limits(dicts, False)
                high_limits.insert(1, "")
                header_labels.append(tuple(high_limits[:err_index]))
                # print("hl len: ", len(high_limits))

            max_values = lf.get_maxs(dicts)
            max_values.insert(1, "")
            
            header_labels.append(tuple(max_values[:err_index]))
            # print("max len: ", len(max_values))
            min_values = lf.get_mins(dicts)
            min_values.insert(1, "")
            header_labels.append(tuple(min_values[:err_index]))
            # print("min len: ", len(min_values))

            mean_values = lf.get_means(dicts)
            mean_values.insert(1, "")
            header_labels.append(tuple(mean_values[:err_index]))

            dicts_counter += 1

            # print("this are the nest number: ", nest_numbers)

            self.tab_controller.create_tab("Nido: " + str(nest_numbers[dicts_counter-1]), test_names, set_of_values, test_limits)

            # print("header:", header_labels)
            return tuple(header_labels), set_of_values
        except Exception as err:
            show_error(err, "excel conversion error")




    def update_progress_bar(self, actual_iteracion, total_iterations, left_bars_text = ''):

        new = (actual_iteracion * 100) / total_iterations

        self.root.update_idletasks()
        new += 0.1
        new = min([new, 100])
        self.pb1['value'] = new

        # pb1_label_text = str(int(0))+'% | ('+ str(idx+1)+"/" + str(amount_of_nests)+")"
        # self.progress_bar_label.config(text=pb1_label_text)
        
        self.progress_bar_label.config(text=str(int(new)) + '%' + left_bars_text)




    def log_to_tree(self, raw_data:str):

        try:

            if raw_data[2:7] != 'BATCH':
                raw_data = raw_data[raw_data.find("{@BATCH"):]

            root = Node('root')

            extract_data = ""

            prev_name = ''
            for idx, char in enumerate(raw_data):

                if char == '{':

                    name = raw_data[idx+2:raw_data.index("|", idx)]


                    if prev_name == 'BTEST':

                        extract_data += '\n'
                    
                    elif prev_name == 'BATCH' and name == 'BTEST':
                        pass
                    elif prev_name == 'BATCH':
                        extract_data += '\n'
                    elif prev_name != 'RPT' and name == 'RPT':
                        extract_data += '\n'

                        # if not self.can_show_fails.get():
                        #     return
                    
                    prev_name = name

                elif char == '}':
                    pass
                    
                else:
                    extract_data += char
            
            new_data_ = extract_data.split("\n\n")


            btch_count = 0

            new_data = []
            for line in new_data_:
                # print("line: ", line)

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
                # print("data: ", data)

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
                        sep_by_newline = data.split("\n")

                        while '' in sep_by_newline:
                            sep_by_newline.remove('')
                        date_container = sep_by_newline[-1].split("|")
                        # print("newlines: ", sep_by_newline)
                        # print("date container: ", date_container)

                        # print("separated data: ", separated_batch_data)

                        raw_date = date_container[3]

                        # print("raw_date: ", raw_date)

                        if len(raw_date) == 12:
                            year = int("20"+raw_date[0:2])
                            month = int(raw_date[2:4])
                            day = int(raw_date[4:6])
                            hour = int(raw_date[6:8])
                            min = int(raw_date[8:10])
                            seg = int(raw_date[10:12])

                            date_ = datetime(year, month, day, hour, min, seg)

                            date_vals = str(self.from_cal.get_date()).split("-")
                            time_vals = timepicker.to_24h_format(self.from_time_lbl['text'])
                            for val in time_vals:
                                date_vals.append(val[:2])

                            from_date = dft.to_date_format(int(date_vals[0]), int(date_vals[1]), int(date_vals[2]), int(date_vals[3]), int(date_vals[4][:2]))
                            # print("from date: ", from_date)
                            # print(date_)

                            date_vals = str(self.to_cal.get_date()).split("-")
                            time_vals = timepicker.to_24h_format(self.to_time_lbl['text'])
                            for val in time_vals:
                                date_vals.append(val[:2])
                            to_date = dft.to_date_format(int(date_vals[0]), int(date_vals[1]), int(date_vals[2]), int(date_vals[3]), int(date_vals[4][:2]))
                            # print("from date: ", to_date)
                            # print(date_vals)

                            if not dft.is_in_date_range(from_date, date_, to_date):

                                return None

                        else:

                            date_ = "N/A"

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

                        # if not self.can_show_empties.get():
                        new_sub_dataset = []
                        for sub_data in new_data[idx+1:]:
                            # print("sub data: ", sub_data)
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

                        # print("new data: ", new_data)

                        for sub_data in new_data:

                            if len(sub_data) > 1:
                                # print("sub data: ", sub_data)
                        

                                name = sub_data[1:sub_data.index("|")]
                                # print("name: ", name)
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
                                                # print("ind data: ", ind_data)
                                                temp_comp_node = Node(comp_name, parent=temp_blck, value=ind_data[2])

                                                limit_name = ''

                                                for d in ind_data:

                                                    if 'LIM' in d:
                                                        limit_name = d
                                                        # print("lim: ", limit_name)
            
                                                if not limit_name == '':
                                                    limits = ind_data[-int(limit_name[-1]):]

                                                    high_lim = limits[-2]
                                                    low_lim = limits[-1]
                                                    measure = ind_data[2]

                                                    # print("low lim: ", low_lim)
                                                    # print("measure: ", measure)
                                                    # print("high lim: ", high_lim)

                                                    
                                                    if not float(low_lim) < float(measure) < float(high_lim):
                                                        
                                                        if not self.can_show_fails.get():
                                                            return None
                                                        else:
                                                            pass
                                                            global failed_tests
                                                            failed_tests.append(t_name)
                                                            temp_comp_node.value += ", FAILED"

                                                            # print("node name: ", temp_comp_node.value)


                                                            

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
    
    


    
    def trees_to_dicts(self, trees):
        
        try:
            dicts = []
            for tree in trees:
                dict = {}
                for batch in tree.children:
                    for idx, block in enumerate(batch.children): #the block has the name of the test
                        if len(block.children) > 1:
                            for comp in block.children:
                                comp_name = "-" + comp.name
                                test_name = block.test_name + comp_name
                                if len(comp.children) > 0:
                                    lims = comp.children[0].value
                                    dict[test_name] = [comp.value, lims]
                                else:
                                    dict[test_name] = [comp.value]
                        else:
                            if len(block.children[0].children) > 0:
                                dict[block.test_name] = [block.children[0].value, block.children[0].children[0].value]
                            else:
                                dict[block.test_name] = [block.children[0].value]
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
            counter = 0
            dfs = []

            files = [('Excel Files', '*.xlsx'), 
                ('All Files', '*.*')]

            file = asksaveasfile(filetypes = files, defaultextension = files)
            if file != None:
                for keys, values in data_dict.items():

                    if keys[1] == 2:
                        keys = keys[0]
                    self.status_label.config(text="sorting the data...",  fg='black')
                    df = convert_to_dataframe(values, keys)
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
                        
                        def set_color(val):
                            val = str(val)
                            # print("this is the val of func: ", val)
                            if "FAILED" in val:
                                if val.split(",")[1] == " FAILED":
                                    return 'background-color:red;text:%s;' % val.split(",")[0]
                                else:
                                    return 'background-color:white;text:0;'
                            else:
                                return 'background-color:white;text:0;'
                        
                        # def remove_failed_str(val):
                        #     str_val = str(val)
                        #     if "FAILED" in str_val:
                        #         val = str_val.split(",")[0]
                        #         return val
                        #     else:
                        #         return val


                        
                        # print(type(df))
                        styled = df.style.applymap(lambda v: set_color(v))
                        
                        # styled = styled.data.applymap(lambda val: remove_failed_str(val))
                        # print("styled: ", styled)

                        styled.to_excel(writer, sheet_name='Nido '+ nest_id, engine='openpyxl')
                
                self.pb1.stop()

                self.set_buttons_state("normal")
                
                self.status_label.config(text="Done!")
                if messagebox.askokcancel(message="La exportacion a excel ha terminado \n¿Desea abrir la ubicacion del archivo?", title= "exportacion terminada"):
                    lf.explore(file.name)
                self.pb1.config(mode="determinate")
            else:
                self.set_buttons_state("normal")
        except Exception as err:
            show_error(err, "export error")
    
    def set_buttons_state(self, state:str):
        self.export_btn["state"] = state
        self.convert_btn["state"] = state
        self.browse_btn["state"] = state
        self.to_time_btn["state"] = state
        self.from_time_btn["state"] = state
        self.check_btn_showempties["state"] = state
        self.check_btn_showdups["state"] = state
        self.check_btn_showfails["state"] = state

    def on_closing(self):

        thread_pool_executor.shutdown()

        self.quit()
        self.destroy()
    
    def highlight_cells(self):
        # provide your criteria for highlighting the cells here
        return ['background-color: yellow']


            
    

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
    

    

        
    
    def create_tab(self, tab_name, test_names:list, set_of_values, test_limits):
        try:
            s = tk.ttk.Style()

            #from os import name as OS_Name
            if root.getvar('tk_patchLevel')=='8.6.9': #and OS_Name=='nt':
                def fixed_map(option):
                    # Fix for setting text colour for Tkinter 8.6.9
                    # From: https://core.tcl.tk/tk/info/509cafafae
                    #
                    # Returns the style map for 'option' with any styles starting with
                    # ('!disabled', '!selected', ...) filtered out.
                    #
                    # style.map() returns an empty list for missing options, so this
                    # should be future-safe.
                    return [elm for elm in s.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]
                s.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))


            test_names[0] = "Serials"
            test_names[1] = "Dates"
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

            for idx, test_name in enumerate(test_names[2:]):
                a = self.my_tn_trees[-1].insert(parent='',index='end',iid=idx,text='aaa', values=test_name, tags=test_name)

            
            global failed_tests

            for fail_test in failed_tests:
                self.my_tn_trees[-1].tag_configure(fail_test, background='red')



            # print("setvals: ", set_of_values)
            self.my_tn_trees[-1].bind('<Double-1>', lambda event,
                                                            tn = test_names[:],
                                                            sv  = set_of_values,
                                                            limits = test_limits,
                                                            :self.tree_click_event(tn, sv, limits))
            

            values_trees_scroll = tk.Scrollbar(temp_tab)
            self.my_trees.append(tk.ttk.Treeview(temp_tab, yscrollcommand=values_trees_scroll.set))
            self.my_trees[-1].pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT)
            values_trees_scroll.pack(side=tk.LEFT, fill=tk.Y)
            values_trees_scroll.config(command=self.my_trees[-1].yview)


            # tree_scroll = tk.Scrollbar(temp_tab)
            # self.my_tn_trees.append(tk.ttk.Treeview(temp_tab, yscrollcommand=tree_scroll.set))
            # self.my_tn_trees[-1].pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT)
            # tree_scroll.pack(side=tk.LEFT, fill=tk.Y)
            # tree_scroll.config(command=self.my_tn_trees[-1].yview)


            test_names_copy = test_names[:7].copy()
            test_names_copy.append("...")
            self.my_trees[-1]["columns"] = test_names_copy
            self.my_trees[-1]['show'] = 'headings'

            

            for idx, test_name in enumerate(test_names_copy):
                self.my_trees[-1].column(test_name ,anchor=tk.CENTER, width=190)
                self.my_trees[-1].heading(test_name,text=test_name)

            
            for idx, vals in enumerate(np.array(set_of_values)[:,:7]):
                new_vals = list(vals)
                new_vals.append("...")
                self.my_trees[-1].insert(parent='',index='end',iid=idx,text='', values=new_vals)
            

            self.my_trees[-1].bind('<Double-1>', lambda event:self.on_values_tree_click(event))
            
        except Exception as err:
            show_error(err, "tab creation error")


    
    def on_values_tree_click(self, event):
        item = self.my_trees[self.tab_index].focus()
        if item != "":
            info = self.my_trees[self.tab_index].item(item, 'values')
            serial = info[0]
            thread_pool_executor.submit(serialreport.show(serial))

    
    def tree_click_event(self, tn, sv, limits):
        set_of_vals = list(np.array(sv)[:])
        
        try:
            item = self.my_tn_trees[self.tab_index].focus()

            if item != "":
                info = self.my_tn_trees[self.tab_index].item(item, 'values')
                test_name = info[0]
                limits = lf.get_test_limits(tn, limits, test_name)

                test_values, serials, dates = lf.get_test_values(tn, set_of_vals, test_name)
                spc.plot(test_values, test_name, limits, serials, dates)
        except Exception as err:
            show_error(err, "show spc error")

        

    def tab_changued(self, event):
        print("tab changued event")
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
    
    

    

class NewWindow(tk.Toplevel):

     
    def __init__(self, master = None, case = None, data = None, ids = None):

        super().__init__(master = master)
        self.title("New Window")
        self.geometry("700x500")


        if case == "export available":
            export_btn = tk.Button(self, text = "Export Now", bg='green')
            export_btn.config(command=lambda : master.export_caller(data, ids))
            export_btn.pack()
    

def convert_to_dataframe(data, cols):
    try:

        new_cols = []

        for col in cols:
            new_cols.append(list(col))

        df = pd.DataFrame(data, columns = new_cols)
        df.index = np.arange(1, len(df)+1)

        return df
    except Exception as e:
        show_error(e, "dataframe creation failed")



if __name__ == "__main__":
    root = tix.Tk()
    main = MainApplication(root)
    root.mainloop()

        





