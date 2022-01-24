
from cgitb import text
import string
from turtle import bgcolor, width
from anytree.node.node import Node
from anytree import RenderTree
import tkinter as tk
from tkinter import tix
import sys, os

import time as tm

from statistics import stdev
from numpy.core.fromnumeric import mean
import pandas as pd
import glob
import os
import re
import numpy as np
import re

from tkinter import filedialog

from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Progressbar

from concurrent import futures
from concurrent import *
import os
import subprocess
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

logs_path = str(" ")
import localfuncs as lf
dicts_counter = 0
amount_of_nests = 0
thread_pool_executor = futures.ThreadPoolExecutor(max_workers=5)

class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.root = root
        self.preview_table = None
        root.geometry('640x220')
        root.title('Logs to excel converter')
        root.iconbitmap("kimball.ico")
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
        self.path_label = tk.Label(self.top_frame, text='Logs path: ', bg='gray94')
        self.path_label.pack(side=tk.LEFT)
        self.textEntryPath = tk.StringVar()
        self.pathEntry = tk.Entry(self.top_frame, textvariable=self.textEntryPath, bg='white')
        self.pathEntry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.textEntryPath.trace("w", lambda name, index,mode, var=self.textEntryPath: self.callback(var))
        self.browse_btn = tk.Button(self.top_frame, text='browse', command=lambda:self.browse_for_path())
        self.browse_btn.pack(side=tk.LEFT,  anchor=tk.NW)
        brws_btn_hover_msg = tix.Balloon(root)
        brws_btn_hover_msg.bind_widget(self.browse_btn, 
        balloonmsg="click to browse the directory of the logs")

        for sub in brws_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')
        
        self.convert_btn = tk.Button(self.top_frame, text='convert', command=lambda:thread_pool_executor.submit(self.log_to_excel_process))
        self.convert_btn.pack(side=tk.LEFT,  anchor=tk.NW)
        self.convert_btn["state"] = "disabled"
        cnvrt_btn_hover_msg = tix.Balloon(root)
        cnvrt_btn_hover_msg.bind_widget(self.convert_btn, 
        balloonmsg="click to start the conversion process")

        for sub in cnvrt_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')

        self.top_frame.pack(fill=tk.BOTH)
        self.middle_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
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

        
    def callback(self, var):
        global logs_path
        logs_path = var.get()
        if var.get() != "":

            self.convert_btn["state"] = "normal"
        else:
            self.convert_btn["state"] = "disabled"


    def browse_for_path(self):
        self.status_label.config(text=" ", bg='gray94',  fg='black')
        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            global logs_path
            logs_path = tempdir
            self.textEntryPath.set(tempdir)


    def log_to_excel_process(self):

        try:
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
                self.show_error(err, "invalid path")
                raise RuntimeError

            self.pb1.config(mode="determinate")
            self.status_label.config(text="formating log files...",  fg='black')
            self.opn_excel_loc.forget()

            for fname in glob.iglob(logs_path + '**/**', recursive=True):

                if os.path.isfile(fname):

                    with open(fname) as log_f:

                        file_name = log_f.name.split("\\")[-1]

                        nest_number = self.get_nest_number(file_name)
                        num_lines = sum(1 for line in open(fname))

                        if not nest_number in set_of_trees:

                            if self.can_show_fails.get():
                                set_of_trees[nest_number] = []
                            else:
                                if num_lines > 30:
                                    set_of_trees[nest_number] = []

                        
            
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
                        # print(RenderTree(tree))

                        num_lines = sum(1 for line in open(fname))
                        if tree != None:
                            if self.can_show_fails.get():
                                set_of_trees[nest_number].append(tree)
                            else:
                                if num_lines > 30:
                                    set_of_trees[nest_number].append(tree)
                        else:
                            print("?")

            data_dict, sheet_ids = self.data_conversion(set_of_trees)
            self.set_buttons_state("normal")


            root.update_idletasks()
            self.pb1['value'] = 100
            self.progress_bar_label.config(text=str(int(100))+'% | ('+ str(dicts_counter)+"/" + str(amount_of_nests)+")")
            self.status_label.config(text="Export is enabled!",  fg='black')

            self.export_btn.config(command=lambda : self.export_caller(data_dict, sheet_ids))
        except Exception as err:
            self.show_error(err, "data extraction error")
        

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

    def data_conversion(self, set_of_trees):
        data_dict = {}
        #temp_tn is refering to a temporal test name, and temp_sv is refering to a temporal set of values
        try:
            for trees in set_of_trees.values():

                temp_tn, temp_sv = self.dicts_to_excel_data(trees_to_dicts(trees))
                if not temp_tn in data_dict:
                    data_dict[tuple(temp_tn)] = temp_sv
                else:
                    data_dict[tuple([temp_tn, 2])] = temp_sv

        except Exception as err:
            self.show_error(err, "data conversion error")
        return data_dict, list(set_of_trees.keys())

        

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
                    if not nest_id is string:
                        nest_id = str(nest_id)

                    df.to_excel(writer, sheet_name='Nido '+ nest_id )
            
            self.pb1.stop()

            self.set_buttons_state("normal")
            
            self.status_label.config(text="Done!", bg='green', fg='white')
            self.opn_excel_loc.config(command=lambda:explore(file.name))
            self.opn_excel_loc.pack(side=tk.LEFT)
            self.pb1.config(mode="determinate")
        except Exception as err:
            self.show_error(err, "export error")
    
    def set_buttons_state(self, state:str):
        self.export_btn["state"] = state
        self.convert_btn["state"] = state
        self.browse_btn["state"] = state

            
    
    def show_error(self, e, tittle_error):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = "     error: {0} \n \
    error type: {1} \n \
    in line: {2}".format(e, exc_type, exc_tb.tb_lineno)
        tk.messagebox.showerror(tittle_error, error)


    def dicts_to_excel_data(self, dicts):

        try:

            self.status_label.config(text='separating by nests...',  fg='black')
            global amount_of_nests
            global dicts_counter
            counter = 0

            test_names = []

            total_iterations = len(get_dicts_only(dicts)[0].keys()) * len(get_dicts_only(dicts)) * 2
            self.pb1.config(mode="determinate")
            
            for dict in get_dicts_only(dicts):

                for test_name in dict.keys():

                    counter += 1
                    left_pbs_str = '| ('+ str(dicts_counter+1)+"/" + str(amount_of_nests)+")"

                    self.update_progress_bar(counter, total_iterations, left_pbs_str)

                    if not test_name in test_names:
                        test_names.append(test_name)
                
            set_of_values = []
            sample_count = 0
            for idx, dict in enumerate(get_dicts_only(dicts)):
                sample_count += 1
                values = []
                for test_name in test_names:

                    counter +=1

                    left_pbs_str = '| ('+ str(dicts_counter+1)+"/" + str(amount_of_nests)+")"

                    self.update_progress_bar(counter, total_iterations, left_pbs_str)

                    if not test_name in list(dict.keys()):
                        # print('NOT FOUND ------------------------')
                        values.append("NONE")
                    else:
                        # print("si hay -----------------------------")
                        values.append(dict[test_name][0])
                
                serial  = get_serials_only(dicts)[idx]
                print("this is a serial: ", serial)
                values.insert(0, serial)
                set_of_values.append(values)
            
            low_limits = lf.get_limits(dicts)
            # print("ll len: ", len(low_limits))
            
            high_limits = lf.get_limits(dicts, False)
            # print("hl len: ", len(high_limits))

            max_values = lf.get_maxs(dicts)
            # print("max len: ", len(max_values))
            min_values = lf.get_mins(dicts)
            # print("min len: ", len(min_values))

            mean_values = lf.get_means(dicts)
            # print("mean len: ", len(mean_values))

            test_names.insert(0, "Test names")

            set_of_vals = np.array(set_of_values)
            # print("vals: ", test_names)

            dicts_counter += 1

            if dicts_counter == amount_of_nests:
                try:
                    self.table_tittle = tk.Label(self.middle_frame, text="Preview table")
                    self.table_tittle.pack(anchor=tk.CENTER)
                    self.preview_table = tk.ttk.Treeview(self.middle_frame)
                    self.preview_table.pack(fill=tk.BOTH, expand=True)
                    self.preview_table['columns']= test_names
                    self.preview_table.column("#0", width=-1300)
                    self.preview_table.heading("#0",text="",anchor=tk.CENTER)
   
                    for test_name in test_names[:10]:
                        self.preview_table.column(test_name ,anchor=tk.CENTER, width=190)
                        self.preview_table.heading(test_name,text=test_name)
                    self.preview_table['show'] = 'headings'

                    for idx, vals in enumerate(np.array(set_of_values)[:10]):
                        self.preview_table.insert(parent='',index='end',iid=idx,text='', values=vals)  
    
                except Exception as err:
                    self.show_error(err, "there was an error")

            return tuple([tuple(test_names), tuple(low_limits), tuple(high_limits), tuple(min_values), tuple(max_values), tuple(mean_values)]), set_of_values
        except Exception as err:
            self.show_error(err, "excel conversion error")




    def update_progress_bar(self, actual_iteracion, total_iterations, left_bars_text = ''):

        new = (actual_iteracion * 100) / total_iterations

        self.root.update_idletasks()
        new += 0.1
        new = min([new, 100])
        self.pb1['value'] = new
        
        self.progress_bar_label.config(text=str(int(new)) + '%' + left_bars_text)




    def log_to_tree(self, raw_data:str):

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
            else:

                new_data.append(line)

        for idx, data in enumerate(new_data):

            if len(data) > 1:
                name = data[1:data.index("|", 1)]
                serial_ = ""
                if name == 'BATCH' or name == '@BATCH':

                    btch_count += 1
                    blck_count = 0

                    if name == '@BATCH':
                        name = name[1:]

                    separated_batch_data = data.split("|")

                    serial_ = separated_batch_data[15] # the value with the index 15 has the serial

                    temp_btch_node = Node(name + str(btch_count), parent=root, serial=serial_)

                    #this loop passes data without mesurments and keeps foreward data with mesurements

                    if not self.can_show_fails.get():
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

                                        if 'LIM' in ind_data[3]:

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
                                pass

        # print("this is the root", RenderTree(root))

        return root
            

def get_dicts_only(dicts):
    dicts_only = []
    for d in dicts:
        dicts_only.append(d[1])
    return dicts_only

def get_serials_only(dicts):
    serials_only = []
    for d in dicts:
        serials_only.append(d[0])
    return serials_only


def trees_to_dicts(trees):

    dicts = []

    for tree in trees:

        dict = {}
        
        for batch in tree.children:
            
            for idx, block in enumerate(batch.children): #the block has the name of the test

                if len(block.children) > 1:
 
                    for comp in block.children:

                        comp_name = "-" + comp.name

                        test_name = block.test_name + comp_name

                        lims = comp.children[0].value

                        dict[test_name] = [comp.value, lims]
                else:

                    if len(block.children[0].children) > 0:

                        dict[block.test_name] = [block.children[0].value, block.children[0].children[0].value]

            dicts.append([batch.serial, dict])  

    return dicts





def convert_to_dataframe(data, cols):
    #de todos los elementos de la lista que se pasa al argumento 'columns' cada elemento es una lista, de la cual en algunos casos se omite el ultimo valor 
    #agregando un [:-1]
    df = pd.DataFrame(data, columns = [list(cols[0]), list(cols[1]), list(cols[2]), list(cols[3]), list(cols[4]), list(cols[5])])
    df.index = np.arange(1, len(df)+1)
    # print("this is df: \n", df)
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
    





