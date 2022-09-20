# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# im p o r t o f n e e d e d l i b r a r i e s
import pandas as pd
import numpy as np
import re
import dateutil.parser as dt
import copy
#increase max print
#pd.set_option('display.max_rows', 10)

# L o a di n g o f d a t a and p r i n t
raw_data = pd.read_csv('personnes.csv')
#retain copy of original data. Deep copy to avoid shared reference
data = copy.deepcopy(raw_data)
print(data)
# Count missing values
print(data.isnull().sum())

# Gives a boolean vector (series, used `type`) of which values are duplicates of
# previous rows
data['email'].duplicated()

#Show all duplicated lines
data.loc[data['email'].duplicated(keep=False),:]

#Define a list of valid countries
validCountries = ['France', 'Côte d\'ivoire', 'Madagascar', 'Bénin', 'Allemagne', 'USA']
#Replace all other countries with 0
data.loc[~data['pays'].isin(validCountries), 'pays'] = np.NaN
print(data)

#Split duplicate emails
#Split into two columns and keep the first
#data['email'] = data['email'].str.split(',',n=1,expand=True)[0]

#Identify values in cm
cm_values = data['taille'].str.contains('cm')

#Extract number
data['taille'] = data['taille'].str.extract('([0-9\.]+)')
#Convert to numeric
data['taille'] = data['taille'].astype('float')
#Convert centimetres to metres
data.loc[cm_values,'taille'] = data.loc[cm_values,'taille'].div(100)

#Now we need to replace these values with the mean of the other ones
#I think this is stupid too, but it's a nice exercise

# def replaceSize(vector, max_size = 3):
  

too_big = data.loc[:,'taille'] > 3
data.loc[too_big,'taille'] = data.loc[~too_big,'taille'].mean()


#Convert dates
# parse doesn't like missing values
# non_missing_dates = ~data['date_naissance'].isnull()
# data.loc[non_missing_dates, 'date_naissance'] = data.loc[non_missing_dates,'date_naissance'].apply(dt.parse)

non_missing_dates = ~data['date_naissance'].isnull()
data.loc[non_missing_dates, 'date_naissance'] = data.loc[non_missing_dates,'date_naissance'].apply(dt.parse)
