## Implements all the preoprocessing steps ##

import pandas
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
import scipy as sp
#from scipy import signal
import csv
#import cvxEDA
from datetime import *
from datetime import timedelta
import pandas
from pandas import DataFrame # In order to write into the .csv file we can use the pandas module
import os


# This function extracts EDA values from the csv file.
# The input of the function is the path of the file, the type of wearable and the signal we are interested in.
def signal_extraction(path, wearable, sign):
    if wearable == "empatica":
        if sign == 'EDA':
            sig = [];

            with open(path, 'rt') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

                for row in spamreader:
                    sig.append(', '.join(row))
          #  print sig
    if wearable == "biovotion":
        if sign == 'EDA':
            db = pandas.read_csv(path)
            time = pandas.to_datetime(db['UTC Timestamp'])
            time = time + timedelta(hours=2)
            sig = pandas.DataFrame({sign :db['Galvanic Skin Response'] , "Time" :time })


    return sig

# This function generates the time for each EDA value based on the first timestamp and the sampling rate.
# First timestamp is the first row in EDA.csv file
# Sampling rate is the second row in EDA.csv file
def time_extraction(signal_array,signal_name):
    i = 0;
    time = [];
    for i in range(0, len(signal_array[3:len(signal_array)])):
        time.append(datetime.fromtimestamp(float(signal_array[0])) + timedelta(minutes=float((i/4.0)/60)))  #the time is expressed in minutes

    signal_time_db = pandas.DataFrame({signal_name:signal_array[3:len(signal_array)], "Time" :time })
    return signal_time_db



#Segmentation
def interval(time, beg, en):
    j = 0;
    interv = [];
    time = pandas.to_datetime(time)
    for j in range(len(time)):
        if time[j] == beg:
            beginning = j
            print(beginning)
        if time[j] == en:
            end = j

    interv = [beginning, end]
    return interv


def part_div(sig, time, start, end):
    interv = interval(time, start, end)  # extract the interval of interest from the time
    part = sig[interv[0]:interv[1]]  # extract the EDA and the time values related to the interval of interest
    return part















# Signal normalization between 0 and 1
def normalization(sig):
    sig = map(lambda x: float(x), sig)
    sig = list(sig)
    normalized = []
    min_val = min(sig)
    max_val = max(sig)

    for i in range(len(sig)):
        normalized.append(((sig[i] - min_val) / (max_val - min_val)))
    return normalized


def filtering(eda, window):
    filtered = sp.signal.medfilt(eda, window)
    return filtered


def windowing(data,fun,window_size,stride):
    result_wind = [fun(data[i:i+window_size]) for i in range(0, len(data), stride)
                   if i+window_size < len(data) ]
    return result_wind
#To filter the noise using the Bartlett filter with a win_size size of the window
    # win_size is the frequency of sensor values

