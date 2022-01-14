
from cgitb import text
from turtle import bgcolor, width
from anytree.node.node import Node
from anytree import RenderTree
import tkinter as tk
from tkinter import tix

import time as tm

from statistics import stdev
from numpy.core.fromnumeric import mean
import pandas as pd
import glob
import os
import re
import numpy as np

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


thread_pool_executor = futures.ThreadPoolExecutor(max_workers=5)


class MainApplication(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.preview_table = None

        root.geometry('500x160')
        root.title('Logs to excel converter')
        root.configure(background='gray94')

        
        self.upper_top_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.export_btn = tk.Button(self.upper_top_frame, text='Export to excel')
        self.export_btn.pack(side=tk.RIGHT)
        self.export_btn["state"] = "disabled"

        self.opn_excel_loc = tk.Button(self.upper_top_frame, text='Open excel location')

        self.can_show_fails = tk.IntVar()
        self.check_btn_showerror = tk.Checkbutton(self.upper_top_frame, text = "Show failed logs?", variable = self.can_show_fails, onvalue = 1, offvalue = 0)
        self.check_btn_showerror.pack(side=tk.RIGHT)

        self.upper_top_frame.pack(fill=tk.BOTH)

        self.top_frame = tk.Frame(root, bg='gray94', highlightthickness=2)
        self.path_label = tk.Label(self.top_frame, text='Logs path: ', bg='gray94')
        self.path_label.pack(side=tk.LEFT)

        self.textEntryPath = tk.StringVar()
        self.pathEntry = tk.Entry(self.top_frame, textvariable=self.textEntryPath, bg='white')
        self.pathEntry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.browse_btn = tk.Button(self.top_frame, text='browse', command=lambda:self.browse_for_path())
        self.browse_btn.pack(side=tk.LEFT,  anchor=tk.NW)

        brws_btn_hover_msg = tix.Balloon(root)
        brws_btn_hover_msg.bind_widget(self.browse_btn, 
        balloonmsg="click to browse the directory of the logs")

        for sub in brws_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')
        
        
        self.convert_btn = tk.Button(self.top_frame, text='convert', command=lambda:thread_pool_executor.submit(self.log_to_excel_process))
        self.convert_btn.pack(side=tk.LEFT,  anchor=tk.NW)

        cnvrt_btn_hover_msg = tix.Balloon(root)
        cnvrt_btn_hover_msg.bind_widget(self.convert_btn, 
        balloonmsg="click to start the conversion process")

        for sub in cnvrt_btn_hover_msg.subwidgets_all():
            sub.config(bg='grey')

        self.top_frame.pack(fill=tk.BOTH)


        self.middle_frame = tk.Frame(root, bg='gray94', highlightthickness=2)

        

        

        


        

        self.bottom_frame = tk.Frame(root, bg='gray94', highlightthickness=2)

        self.pb1 = Progressbar(self.bottom_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.pb1.pack(side=tk.BOTTOM, anchor=tk.NW, fill=tk.X, expand=True, pady=2, padx=2)

        self.status_label = tk.Label(self.bottom_frame, text=' ', bg='gray94')
        self.status_label.pack(side=tk.LEFT, anchor=tk.SW)

        self.bottom_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.status_label.config(text=" ", bg='gray94')

        

        

       
        self.middle_frame.pack(fill=tk.BOTH, expand=True)

        

    def browse_for_path(self):
        if self.preview_table != None:
            self.preview_table.destroy()
            self.table_tittle.destroy()
        # self.preview_table.delete(*self.preview_table.get_children())
        global dicts_counter
        dicts_counter = 0
        self.status_label.config(text=" ", bg='gray94')
        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            global logs_path
            logs_path = tempdir
            self.textEntryPath.set(tempdir)
            global pathEntry

            
            


    def log_to_excel_process(self):
        

        set_of_trees = [[], [], [], []]


        

        print("init")
        counter = 0
        all_files = [name for name in os.listdir(logs_path) if os.path.isfile(os.path.join(logs_path, name))]
        

        self.pb1.config(mode="determinate")
        self.status_label.config(text="processing log files...")
        self.opn_excel_loc.forget()

        print("starting point: ", len(all_files))
        tm.sleep(1)
        for fname in glob.iglob(logs_path + '**/**', recursive=True):

            new = (counter * 100) / len(all_files)
            counter += 1
            root.update_idletasks()
            self.pb1['value'] = new
            # print(new)
            


            if os.path.isfile(fname):
                num_lines = sum(1 for _ in open(fname))
                with open(fname) as log_f:

                    # start_of_log_f = log_f.name[:2]

                    # if start_of_log_f == r'[1-9]-':
                    #     raw_data = log_f.read()
                        
                    #     if num_lines > 26:
                    #         tree = log_to_tree(raw_data)
                    #         if tree != None:
                    #             set_of_trees[int(start_of_log_f[:1])]
                    #             trees1.append(tree)


                    
                    if '1-' in log_f.name:
                        
                        raw_data = log_f.read()
                        
                        if num_lines > 26:
                            tree = self.log_to_tree(raw_data)
                            # print(RenderTree(tree))
                            if tree != None:
                                set_of_trees[0].append(tree)
                        elif self.can_show_fails.get():
                            tree = self.log_to_tree(raw_data)
                            # print(RenderTree(tree))
                            if tree != None:
                                set_of_trees[0].append(tree)

                    elif '2-' in log_f.name:
                        raw_data = log_f.read()
                        if num_lines > 26:
                            tree = self.log_to_tree(raw_data)
                            if tree != None:
                                set_of_trees[1].append(tree)
                        elif self.can_show_fails.get():
                            tree = self.log_to_tree(raw_data)
                            # print(RenderTree(tree))
                            if tree != None:
                                set_of_trees[1].append(tree)

                    elif '3-' in log_f.name:
                        raw_data = log_f.read()
                        if num_lines > 26:
                            tree = self.log_to_tree(raw_data)
                            if tree != None:
                                set_of_trees[2].append(tree)
                        elif self.can_show_fails.get():
                            tree = self.log_to_tree(raw_data)
                            # print(RenderTree(tree))
                            if tree != None:
                                set_of_trees[2].append(tree)

                    elif '4-' in log_f.name:
                        raw_data = log_f.read()
                        
                        if num_lines > 26:
                            tree = self.log_to_tree(raw_data)
                            if tree != None:
                                set_of_trees[3].append(tree)
                        elif self.can_show_fails.get():
                            tree = self.log_to_tree(raw_data)
                            # print(RenderTree(tree))
                            if tree != None:
                                set_of_trees[3].append(tree)
                    else:
                        raw_data = log_f.read()
                        
                        if num_lines > 26:
                            tree = self.log_to_tree(raw_data)
                            if tree != None:
                                set_of_trees[3].append(tree)
                        elif self.can_show_fails.get():
                            tree = self.log_to_tree(raw_data)
                            # print(RenderTree(tree))
                            if tree != None:
                                set_of_trees[3].append(tree)

    
        
        print("starting last pb")
        self.pb1.config(mode="indeterminate")
        self.pb1.start(10)
        # print("this are the set of trees: ", set_of_trees)


        data_dict = self.data_conversion(set_of_trees)


        self.export_btn["state"] = "normal"
        self.status_label.config(text="Export is enabled!")
        self.pb1.config(mode="determinate")
        self.pb1['value'] = 100
        self.export_btn.config(command=lambda : self.export_caller(data_dict))
    
    def data_conversion(self, set_of_trees):

        # print("this are the set of trees: ", set_of_trees)
        data_dict = {}
        #tn is refering to test_name, and sv is refering to 'set of values'

        for trees in set_of_trees:
            temp_tn, temp_sv = self.dicts_to_excel_data(trees_to_dicts(trees))
            data_dict[tuple(temp_tn)] = temp_sv

        self.pb1.stop()
        return data_dict

        

    def export_caller(self, dicts_data):
        thread_pool_executor.submit(self.export_to_excel, dicts_data)

    
    def export_to_excel(self, data_dict):
        self.export_btn["state"] = "disabled"
        counter = 0
        dfs = []

        files = [('Excel Files', '*.xlsx'), 
             ('All Files', '*.*')]

        file = asksaveasfile(filetypes = files, defaultextension = files)
        for key, value in data_dict.items():
            self.status_label.config(text="sorting the data...")
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
                status_text = "creating sheet " + "(" + str(idx+1) + "/" + str(len(new_dfs)) + ") ..."
                self.status_label.config(text=status_text)
                counter += 1
                df.to_excel(writer, sheet_name='Nido '+ str(counter))  
        
        self.pb1.stop()
        self.export_btn["state"] = "normal"
        
        self.status_label.config(text="Done!", bg='green')
        self.opn_excel_loc.config(command=lambda:explore(file.name))
        self.opn_excel_loc.pack(side=tk.LEFT)
        self.pb1.config(mode="determinate")

    def dicts_to_excel_data(self, dicts):
        global dicts_counter
        
        # print("this are the dicts: ", dicts)
        
        test_names = []

        for dict in get_dicts_only(dicts):
            # print("this should be a dict: ", )
            for test_name in dict.keys():
                # print(test_name)
                if not test_name in test_names:
                    test_names.append(test_name)
            
        set_of_values = []
        sample_count = 0
        for dict in get_dicts_only(dicts):
            sample_count += 1
            values = []
            for test_name in test_names:
                if not test_name in list(dict.keys()):
                    # print('NOT FOUND ------------------------')
                    values.append("NONE")
                else:
                    # print("si hay -----------------------------")
                    values.append(dict[test_name][0])

            serial  = get_serials_only(dicts)[get_dicts_only(dicts).index(dict)]
            # print("this is a serial: ", serial)
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
        # stdev_values = lf.get_stdevs(dicts)
        # print("stdev len: ", len(stdev_values))

        # cpk_values = lf.cpks(high_limits, mean_values, stdev_values, low_limits)
        # print("cpk len: ", len(cpk_values))

        test_names.insert(0, "Test names")

        

        

        
        if dicts_counter < 1:
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

                for idx, vals in enumerate(np.array(set_of_values)[:,:10]):
                    self.preview_table.insert(parent='',index='end',iid=idx,text='', values=vals)  
  
                
            except Exception as err:
                print("there was an error: ", err)
        
        dicts_counter += 1



        

        return tuple([tuple(test_names), tuple(low_limits), tuple(high_limits), tuple(min_values), tuple(max_values), tuple(mean_values)]), set_of_values

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

                

                # print("name of line: ", name)

                if name == 'BLOCK':
                    blck_counter += 1


                
                # print("name of line: ", name)
                if prev_name == 'BTEST':
                    # print(name)
                    extract_data += '\n'
                
                elif prev_name == 'BATCH' and name == 'BTEST':
                    pass
                    # extract_data += '\n'
                elif prev_name == 'BATCH':
                    extract_data += '\n'


                
                prev_name = name

                
            elif char == '}':
                pass
                
            else:
                extract_data += char
        
        if blck_counter == 0:
            # print("block counter: ", blck_counter)
            return None
            
        new_data_ = extract_data.split("\n\n")


        btch_count = 0

        # print("this is new data: ", new_data_)




        # print("about to show lines")
        new_data = []
        for line in new_data_:
            # print(line)
            
            name = line[1:3]
            

            if 'ET' in line:
                pass
            elif name == 'PF' or name == 'TS':
                pass
            elif line[1:6] == 'BTEST':
                # print("this line has the serial: ", line)
                pass
            elif line[1:5] == 'TJET':
                pass
            else:

                new_data.append(line)

        # print("this is new data: ", new_data)



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
                    # print("this is the separated batch data: ", separated_batch_data)
                    # print("------------------------------------------")

                    serial_ = separated_batch_data[15] # the value with the index 15 has the serial

                    temp_btch_node = Node(name + str(btch_count), parent=root, serial=serial_)

                    

                    let_continue = False
                    #this loop passes data without mesurments and keeps foreward data with mesurements


                    if not self.can_show_fails.get():
                        new_sub_dataset = []
                        for sub_data in new_data[idx+1:]:
                            if len(sub_data) > 1:
                                name = sub_data[1:sub_data.index("|")]
                                ind_data = sub_data.split('|')

                                # if '@RTP' in ind_data[2]:
                                #     let_continue = True
                                #     break
                                if len(ind_data) > 2:
                                    if "@A" in ind_data[2]:
                                        if name.startswith("@"):
                                            sub_data = sub_data[1:]
                                        else:
                                            pass
                                        new_sub_dataset.append(sub_data)
                                    # print("name: ", ind_data)
                        # new_sub_dataset.insert(0, 0)
                        new_data = new_sub_dataset
                    if let_continue:
                        pass
                        # continue

                    for sub_data in new_data:
                        # print("this is subdata: ", sub_data)
                        if len(sub_data) > 1:
                            name = sub_data[1:sub_data.index("|")]
                            # print('this is spmething: ', name)
                            if name == 'BLOCK':

                                blck_count += 1

                                block_data = sub_data.split('\n')[1:]

                                t_name = sub_data.split('\n')[0].split('|')[1]

                                temp_blck = Node(name + str(blck_count), parent=temp_btch_node, test_name=t_name)

                                for b_data in block_data:
                                    # print("this is b data", b_data)
                                    ind_data = b_data.split('|') # indidual data or separated data 
                                    
                                    

                                    new_ind_data = [] #re-process data to be separated again if necessary

                                    for d in ind_data:


                                        if 'LIM' in d:
                                            split_d = d.split("@")
                                            for sd in split_d:
                                                new_ind_data.append(sd)
                                        else:
                                            new_ind_data.append(d)

                                    
                                    # print("this is the new individual data: ", new_ind_data)

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
        # print("this is serial and dict: ", d)
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
        batch_dict = {}
        dict = {}
        serial = ''
        
        for batch in tree.children:
            
            for idx, block in enumerate(batch.children): #the block has the name of the test

                if len(block.children) > 1:
 
                    for comp in block.children:
                        # if len(comp.children) > 0
   

                        comp_name = "-" + comp.name

                        test_name = block.test_name + comp_name


                        # print("this is the comp", comp)

                        lims = comp.children[0].value

                        dict[test_name] = [comp.value, lims]
                else:



                    if len(block.children[0].children) > 0:

                        dict[block.test_name] = [block.children[0].value, block.children[0].children[0].value]


        
            # print("this is the serial before append: ", serial)
            dicts.append([batch.serial, dict])
            # batch_dict[serial] = dict
            # dicts.append(batch_dict[serial])   
    return dicts





def convert_to_dataframe(data, cols):
    #de todos los elementos de la lista que se pasa al argumento 'columns' cada elemento es una lista, de la cual en algunos casos se omite el ultimo valor 
    #agregando un [:-1]
    df = pd.DataFrame(data, columns = [list(cols[0]), list(cols[1]), list(cols[2]), list(cols[3]), list(cols[4]), list(cols[5])])
    print("this is df: \n", df)
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
    






#old convert to datafame func

# def convert_to_dataframe(data, cols):
#     new_data = []


#     for d in data:
#         new_data.append(d)

    
#     for col in cols:
#         pass
#         # print(len(col))
    
#     #de todos los elementos de la lista que se pasa al argumento 'columns' cada elemento es una lista, de la cual en algunos casos se omite el ultimo valor 
#     #agregando un [:-1]
#     df = pd.DataFrame(new_data, columns = [list(cols[0]), list(cols[1]), list(cols[2]), list(cols[3]), list(cols[4]), list(cols[5]), list(cols[6]), list(cols[7])])
#     print("this is df: \n", df)
#     return df