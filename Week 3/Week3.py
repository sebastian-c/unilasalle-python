# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:24:37 2022

@author: Sebastian
"""

import pandas as pd
import copy as cp
import numpy as np
#import statmodels.ECDF as ECDF

from matplotlib import pyplot as plt

### LESSON 1

raw_data = pd.read_csv("Week 2/Week2.csv")
data = cp.deepcopy(raw_data)

data["abs_montant"] = data["montant"].abs()

# Make sure that log accepts nan values
old = np.seterr(invalid='ignore')
# Add new column to take the log of montant
data["log_montant"] = np.log10(data["montant"])
# Clean up - reset settings to how they were
np.seterr(**old)

dm = data["montant"]

dm.mean()
dm.median()
dm.mode()
dm.var()
dm.var(ddof=0) #sample variance
dm.std()
dm.skew()
dm.kurtosis()

#Create arbitrary quat
dm.quantile(np.linspace(0.0,1.0,6,endpoint=True))



data.boxplot("montant", vert = False)

###########
# Set the figure size
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

data.boxplot("log_montant", vert = False)
############

data.boxplot(["montant", "log_montant"], vert = False)

## Absolute mean difference
def AbsMeanDifference(x):
    x0 = x.dropna().reset_index(drop = True)
    y = np.sum(np.abs(x0 - x0.median()))/x0.size
    return(y)

def AbsMeanDifferenceLoop(x):
    x0 = x.dropna().reset_index(drop = True)
    m = x0.median()
    s = x0.size
    y = pd.Series([], dtype = "float64")
    for i in range(1, s):
        y[i] = np.abs(x0[i] - m)/s
    return(np.sum(y))


AbsMeanDifference(data["montant"])
AbsMeanDifferenceLoop(data["montant"])

#pd.ECDF(data["montant"])

depenses = data["montant"][data["montant"] < 0]
depenses = -depenses

n = depenses.size

lorenz = np.cumsum(np.sort(depenses))/depenses.sum()
lorenz = np.append(0,lorenz) #Lorenz curve starts at 0

#n+1 because of the extra 0 we added
xaxis = np.linspace(0, 1, n+1, endpoint=True)

plt.plot(xaxis, lorenz, drawstyle = 'steps-post')


### LESSON 2


