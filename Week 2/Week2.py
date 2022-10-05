# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 09:23:20 2022

@author: Sebastian
"""

import pandas as pd
import numpy as np
import copy as cp
#import plotnine as gg

raw_data = pd.read_csv("Week 2/operations.csv", parse_dates = ["date_operation"])
data  = cp.deepcopy(raw_data)

data_categ_freq = data["categ"].value_counts(normalize=True)
data_categ_freq.plot(kind = "pie")
data_categ_freq.plot(kind = "bar")

# Create quarter
# data["quarter_year"] = pd.PeriodIndex(data["date_operation"], freq='Q')
# data["quarter"] = data["quarter_year"].strftime('%q')
#data["quarter"] = data.quarter.astype("int")""
#data["date_operation"] = pd.to_datetime(data["date_operation"])
data["quarter_month"] = [int((day-1)*4/31)+1 for day in data["date_operation"].dt.day]

#data["date_operation"].dt.day
#quart = for i in datq
#data["quarter_month"] = data[]


#Histogram
data[data.montant.abs() < 100]["montant"].hist(density = True, bins=20)

# Cumulative

number = data["quarter_month"].value_counts()

#write data to be used by subsequent weeks
data.to_csv("Week2.csv")

# How to make function
# def fun(x):
#     return(x*2)

# n = [1,4,6,8,2]

# for i in n:
#     print("Input: " + str(i) + ", Calculated: " + str(fun(i)))

