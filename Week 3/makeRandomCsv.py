# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 11:00:01 2022

@author: Sebastian
"""

import numpy as np
import pandas as pd


def makeRandomCsv(slope=-10,
                  intercept=10,
                  noise_sd=1,
                  n_values=100,
                  range_min=1,
                  range_max=100,
                  x_name="x",
                  y_name="y",
                  csv_name="data.csv",
                  include_rownames=False):

    x = np.linspace(range_min, range_max, n_values)

    # make y value with model and random noise
    y_fitted = slope * x + intercept
    y_error = np.random.normal(0, noise_sd, n_values)
    y = y_fitted + y_error

    data = pd.DataFrame(np.transpose([x, y]), columns=[x_name, y_name])

    data.to_csv(csv_name, index=include_rownames)

    return(csv_name)


# Make random csv with default parameters
makeRandomCsv()
# make random csv with 1000 values with a different name
makeRandomCsv(n_values=1000, csv_name="data2.csv")
