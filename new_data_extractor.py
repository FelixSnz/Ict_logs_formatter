
from anytree.node.node import Node
from anytree import RenderTree
import tkinter as tk

from statistics import stdev
from numpy.core.fromnumeric import mean
import pandas as pd
import glob
import os

from tkinter import filedialog

from tkinter.filedialog import asksaveasfile
from tkinter.ttk import Progressbar


import localfuncs as lf


# class MainApplication(tk.Frame):
#     def __init__(self, root, *args, **kwargs):
#         tk.Frame.__init__(self, root, *args, **kwargs)

#         self.pb1 = Progressbar(self.bottom_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
#         self.pb1.pack(side=tk.LEFT, anchor='sw', pady=2, padx=2)
#         pass


def main():

    trees1 = []
    trees2 = []
    trees3 = []
    trees4 = []

    logs_path = browse_for_path()

    for fname in glob.iglob(logs_path + '**/**', recursive=True):
        if os.path.isfile(fname):
            num_lines = sum(1 for _ in open(fname))
            with open(fname) as log_f:

                
                if '1-' in log_f.name:
                    
                    raw_data = log_f.read()
                    
                    if num_lines > 26:
                        tree = log_to_tree(raw_data)
                        if tree != None:
                            trees1.append(tree)
                elif '2-' in log_f.name:
                    raw_data = log_f.read()
                    if num_lines > 26:
                        tree = log_to_tree(raw_data)
                        if tree != None:
                            trees2.append(tree)

                elif '3-' in log_f.name:
                    raw_data = log_f.read()
                    if num_lines > 26:
                        tree = log_to_tree(raw_data)
                        if tree != None:
                            trees3.append(tree)

                elif '4-' in log_f.name:
                    raw_data = log_f.read()
                    
                    if num_lines > 26:
                        tree = log_to_tree(raw_data)
                        if tree != None:
                            trees4.append(tree)
                else:
                    raw_data = log_f.read()
                    
                    if num_lines > 26:
                        tree = log_to_tree(raw_data)
                        if tree != None:
                            trees4.append(tree)


    

    data_dict = {}

    #tn is refering to test_name, and sv is refering to 'set of values'

    tn1, sv1 = dicts_to_excel_data(trees_to_dicts(trees1))

    data_dict[tn1] = sv1

    tn2, sv2 = dicts_to_excel_data(trees_to_dicts(trees2))

    data_dict[tn2] = sv2

    tn3, sv3 = dicts_to_excel_data(trees_to_dicts(trees3))

    data_dict[tn3] = sv3

    tn4, sv4 = dicts_to_excel_data(trees_to_dicts(trees4))

    data_dict[tuple(tn4)] = sv4



    export_to_excel(data_dict) #al llamar esta funcion, se pide una ruta donde guardar los datos en formato xls


def browse_for_path():
        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:


        
            return tempdir

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

def dicts_to_excel_data(dicts):
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
    stdev_values = lf.get_stdevs(dicts)
    # print("stdev len: ", len(stdev_values))

    cpk_values = lf.cpks(high_limits, mean_values, stdev_values, low_limits)
    # print("cpk len: ", len(cpk_values))

    test_names.insert(0, "Test names")

    return tuple([tuple(test_names), tuple(low_limits), tuple(high_limits), tuple(stdev_values), tuple(cpk_values), tuple(min_values), tuple(max_values), tuple(mean_values) ]), set_of_values




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




def export_to_excel(data_dict):
        counter = 0
        dfs = []

        files = [('Excel Files', '*.xlsx'), 
             ('All Files', '*.*')]

        file = asksaveasfile(filetypes = files, defaultextension = files)
        for key, value in data_dict.items():
            df = convert_to_dataframe(value, key)
            dfs.append(df)
        
        new_dfs = []
        for idx, df in enumerate(dfs):
            if not df.empty:
                new_dfs.append(df)
        with pd.ExcelWriter(file.name) as writer: 
            for df in new_dfs:
                counter += 1
                df.to_excel(writer, sheet_name='Nido '+ str(counter))  

                






def convert_to_dataframe(data, cols):


    
    #de todos los elementos de la lista que se pasa al argumento 'columns' cada elemento es una lista, de la cual en algunos casos se omite el ultimo valor 
    #agregando un [:-1]
    df = pd.DataFrame(data, columns = [list(cols[0]), list(cols[1]), list(cols[2]), list(cols[3]), list(cols[4]), list(cols[5]), list(cols[6]), list(cols[7])])
    print("this is df: \n", df)
    return df



def log_to_tree(raw_data:str):


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

                new_sub_dataset = []


                #this loop passes data without mesurments and keeps foreward data with mesurements
                for sub_data in new_data[idx+1:]:
                    if len(sub_data) > 1:
                        name = sub_data[1:sub_data.index("|")]
                        ind_data = sub_data.split('|')

                        if "@A" in ind_data[2]:
                            if name.startswith("@"):
                                sub_data = sub_data[1:]
                            else:
                                pass
                            new_sub_dataset.append(sub_data)
                        # print("name: ", ind_data)


                for sub_data in new_sub_dataset:
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






if __name__ == "__main__":
    root = tk.Tk()
    # main = MainApplication(root)
    main()






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