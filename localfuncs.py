from ast import While
from statistics import stdev
from numpy.core.fromnumeric import mean
import tkinter as tk
import sys, os
import subprocess
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

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

def to_float(str_data):
    float_list = []

    for str in str_data:
        float_list.append(float(str))
    
    return float_list

def reduce_limits(duplic_limits):
    new_limits = []
    for limits in duplic_limits:
        for limit in limits:
            new_limits.append(limit)
            break
    return new_limits

def get_limits(dicts, low_limits=True):

    try:

        test_names = []

        for dict in get_dicts_only(dicts):
            for test_name in dict.keys():
                if not test_name in test_names:
                    test_names.append(test_name)

        # print("this are the test names: ", test_names)
        dict_results = {}
        limit_counter = 0
        for test_name in test_names:
            values = []
            for dict in get_dicts_only(dicts):
                if bool(dict) and test_name in list(dict.keys()):

                    if low_limits:
                        if len(dict[test_name][1]) == 2:
                            limit = dict[test_name][1][0]
                            values.append(limit)
                        
                        else:
                            limit = dict[test_name][1][1]
                            values.append(limit)
                    else:
                        if len(dict[test_name][1]) == 2:
                            limit = dict[test_name][1][1]
                            values.append(limit)
                        
                        else:
                            limit = dict[test_name][1][2]
                            values.append(limit)
                else:
                    limit_counter +=1

            dict_results[test_name] = values

        limits = []
        for val in dict_results.values():

            limits.append(to_float(val))

        limits = reduce_limits(limits)
        if low_limits:
            limits.insert(0, "High Limits")
        else:
            limits.insert(0, "Low Limits")

        return limits
    except Exception as e:
        show_error(e, "get_limits func error")

def show_error(e, tittle_error):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        error = "     error: {0} \n \
    error type: {1} \n \
    in line: {2}".format(e, exc_type, exc_tb.tb_lineno)
        tk.messagebox.showerror(tittle_error, error)  

def get_maxs(dicts):
    try:

        test_names = []

        for dict in get_dicts_only(dicts):
            for test_name in dict.keys():
                if not test_name in test_names:
                    test_names.append(test_name)

        # print("this are the test names: ", test_names)
        dict_results = {}
        for test_name in test_names:
            values = []
            for dict in get_dicts_only(dicts):
                if bool(dict) and test_name in list(dict.keys()):
                    # print("this is the dict: ", dict)
                    val = dict[test_name][0]
                    if val != "FAILED":
                        values.append(val)
            dict_results[test_name] = values

        maxims = []
        
        vals = list(dict_results.values())

        for val in vals:
            print("this is val: ", val)
            maxims.append(max(to_float(val)))
        
        # print(maxims)

        maxims.insert(0, "Max Values")
        return maxims
    except Exception as e:
        show_error(e, "get max values error")

def get_mins(dicts):

    test_names = []

    for dict in get_dicts_only(dicts):
        for test_name in dict.keys():
            if not test_name in test_names:
                test_names.append(test_name)


    dict_results = {}
    for test_name in test_names:
        values = []
        for dict in get_dicts_only(dicts):
            if bool(dict) and test_name in list(dict.keys()):
                val = dict[test_name][0]
                if val != "FAILED":
                    values.append(val)
        dict_results[test_name] = values

    mins = []
    vals = list(dict_results.values())

    for val in vals:
        # print("this is val 0: ", val)
        mins.append(min(to_float(val)))
    
    # print(len(mins))

    mins.insert(0, "Min Values")
    return mins

def get_means(dicts):

    test_names = []

    for dict in get_dicts_only(dicts):
        for test_name in dict.keys():
            if not test_name in test_names:
                test_names.append(test_name)


    dict_results = {}
    for test_name in test_names:
        values = []
        for dict in get_dicts_only(dicts):
            if bool(dict) and test_name in list(dict.keys()):
                val = dict[test_name][0]
                if val != "FAILED":
                    values.append(val)
        dict_results[test_name] = values

    means = []
    vals = list(dict_results.values())

    for val in vals:
        print(val)

        means.append(mean(to_float(val)))
    


    means.insert(0, "Mean Values")
    return means

def get_stdevs(dicts):

    test_names = []

    for dict in get_dicts_only(dicts):
        for test_name in dict.keys():
            if not test_name in test_names:
                test_names.append(test_name)

    dict_results = {}
    for test_name in test_names:
        values = []
        for dict in get_dicts_only(dicts):
            if bool(dict) and test_name in list(dict.keys()):
                values.append(dict[test_name][0])
        dict_results[test_name] = values

    stdevs = []
    for val in dict_results.values():

        stdevs.append(stdev(to_float(val)))

    stdevs.insert(0, "stdev Values")
    return stdevs

def get_test_limits(test_names, set_of_values, limits_test_name):
    try:

        limits_idx = 0

        for idx, test_name in enumerate(test_names):
            if test_name == limits_test_name:
                limits_idx = idx
                break
        

        return set_of_values[limits_idx -2]
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

        serials.append(values[0])
        dates.append(values[1])
        test_values.append(values[values_idx])
    
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





def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])








def cpks(h_limits, means, stdevs, l_limits):

    means =  to_float(means[1:])

    # print("this are limits: ", reduce_limits(h_limits)[1:])

    h_limits = h_limits[1:]

    l_limits = l_limits[1:]

    stdevs = to_float(stdevs[1:])


    cpks = []

    for idx in range(0, len(means)):
        # cpk = min([(h_limits[idx] - means[idx])/(3*stdevs[idx]), (means[idx] - l_limits[idx])/(3 * stdevs[idx])]) temporal comment
        pass
        # cpks.append(cpk) temporal comment
        cpks.append(0)

    
    
    cpks.insert(0, "Cpk Values")

    return cpks


