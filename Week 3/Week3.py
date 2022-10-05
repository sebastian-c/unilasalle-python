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
data["log_montant"] = np.log10(abs(data["montant"]))
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

#Create arbitrary quant
dm.quantile(np.linspace(0.0,1.0,6,endpoint=True))

#data.boxplot("montant", vert = False)
#data.boxplot("log_montant", vert = False)

############ Dual plot
# Set the figure size
# plt.rcParams["figure.figsize"] = [7.50, 3.50]
# plt.rcParams["figure.autolayout"] = True

#data.boxplot(["montant", "log_montant"], vert = False)

## Absolute mean difference
def AbsMeanDifference(x):
    # remove NAs and reset the index numbers
    x0 = x.dropna().reset_index(drop = True)
    y = np.sum(np.abs(x0 - x0.median()))/x0.size
    return(y)

def AbsMeanDifferenceLoop(x):
    # remove NAs and reset the index numbers
    # - If you don't do this, the loop will
    #   fail when it reaches the gap left by 
    #   the first NaN.
    x0 = x.dropna().reset_index(drop = True)
    m = x0.median()
    s = x0.size
    y = pd.Series([], dtype = "float64")
    for i in range(0, s):
        y[i] = np.abs(x0[i] - m)
    ret = np.sum(y)/s
    return(ret)


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

depenses = data.loc[data["montant"] < 0, :]
depenses.loc[:,["montant"]] = depenses.loc[:,["montant"]] * -1


tailleClasse = 500 # taille des classes pour la sicrétisation

groupes = [] #va recevoir les données agrégées à afficher

#on calcule des tranches allant de 0 au solde maximum par paliers de taille tailleClasses

tranches = np.arange(0, max(depenses["solde_avt_ope"]),tailleClasse)

tranches += tailleClasse/2 #☻ on décale les tranches d'une demi taille de classe

indices = np.digitize (depenses["solde_avt_ope"],tranches) #associe chaque solde à son numéro de classe

for ind, tr in enumerate (tranches):#pour chaque tranche ind reçoit le numéro et tr de la tranche en question

    montants =-depenses.loc[indices==ind,"montant"] #sélection des individus de la tranche ind

    if len(montants) > 0:

        g = {

            'valeurs' : montants,

            'centreClasse' : tr-(tailleClasse/2),

            'taille' : len(montants),

            'quartiles' : [np.percentile (montants,p) for p in [25,50,75]]

            }

        groupes.append (g)

plt.figure(figsize =(10,7))

#affichage des boxplots

plt.boxplot ([g["valeurs"]for g in groupes],

              positions = [g["centreClasse"]for g in groupes], #abscisses des boxplotes

              showfliers = False, #on ne prend pas en compte les outliers

              widths = tailleClasse*0.7) #largeur graphique des boxplots

#affichage des effectifs de chaque classe

for g in groupes :

    plt.text(g["centreClasse"],0,"(n={})".format(g["taille"]), horizontalalignment ='center', verticalalignment='top')

    plt.show()
