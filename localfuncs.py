from statistics import stdev
from numpy.core.fromnumeric import mean
import tkinter as tk
import sys

def get_dicts_only(dicts):
    dicts_only = []
    for d in dicts:
        # print("this is serial and dict: ", d[1])
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
    # print("duplic: d", duplic_limits)
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
                    # print("this is the dict: ", dict)
                    # print("this is the test: ", test_name)
                    # print("this are the limits: ", dict[test_name])
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
                    # print("quesestoio9oo")
                    # values.append(dict[test_name][1])
            dict_results[test_name] = values

        limits = []
        for val in dict_results.values():
            # print("this is val 0: ", val)
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
                values.append(dict[test_name][0])
        dict_results[test_name] = values

    maxims = []
    for val in dict_results.values():
        # print("this is val 0: ", val)
        maxims.append(max(to_float(val)))
    
    # print(maxims)

    maxims.insert(0, "Max Values")
    return maxims

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
                values.append(dict[test_name][0])
        dict_results[test_name] = values

    mins = []
    for val in dict_results.values():
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
                # print("this is the dict: ", dict)
                values.append(dict[test_name][0])
        dict_results[test_name] = values

    means = []
    for val in dict_results.values():
        # print("this is val 0: ", val)
        means.append(mean(to_float(val)))
    
    # print(means)

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
                # print("this is the dict: ", dict)
                values.append(dict[test_name][0])
        dict_results[test_name] = values

    stdevs = []
    for val in dict_results.values():
        # print("this is val 0: ", val)
        stdevs.append(stdev(to_float(val)))
    
    # print(len(mins))

    stdevs.insert(0, "stdev Values")
    return stdevs





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


