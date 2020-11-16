#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
import sklearn.model_selection
import sklearn.model_selection
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import networkx as nx
from itertools import product
from pulp import LpVariable, lpSum, value
from ortoolpy import model_min, addvars, addvals

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load data
df_tc = pd.read_csv('trans_cost.csv', index_col="工場")
df_demand = pd.read_csv('demand.csv')
df_supply = pd.read_csv('supply.csv')

# initial configuration
np.random.seed(1)
nw = len(df_tc.index)
nf = len(df_tc.columns)
pr = list(product(range(nw), range(nf)))

# generate mathmatical model
m1 = model_min()  # declare model purpose as minimization
v1 = {(i, j): LpVariable('v%d_%d' % (i, j), lowBound=0)
      for i, j in pr}  # define the primary variable v1
m1 += lpSum(df_tc.iloc[i][j] * v1[i, j]
            for i, j in pr)  # define object function to m1

# add constraint condition
# condition for supply
for i in range(nw):
    m1 += lpSum(v1[i, j] for j in range(nf)) <= df_supply.iloc[0][i]
# condition for demand
for j in range(nf):
    m1 += lpSum(v1[i, j] for i in range(nw)) >= df_demand.iloc[0][j]
m1.solve() # solve minimization problem

# calculate total transportation cost
df_tr_sol = df_tc.copy()
total_cost = 0
for k, x in v1.items():
    i, j = k[0], k[1]
    df_tr_sol.iloc[i][j] = value(x)
    total_cost += df_tc.iloc[i][j] * value(x)

print(df_tr_sol)
print("総輸送コスト：" + str(total_cost))
