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
from ortoolpy import model_min, model_max, addvars, addvals, logistics_network

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load data
df_links = pd.read_csv("links.csv")
# print(df_links.head())

###############################
# visualize 20 users' network #
###############################
# generate graph object
G = nx.Graph()

# set nodes
NUM = len(df_links.index)
for i in range(1, NUM+1):
    node_no = df_links.columns[i].strip("Node")
    # print(node_no)
    G.add_node(str(node_no))

# set edges
for i in range(NUM):
    for j in range(NUM):
        # print(i, j)
        if df_links.iloc[i][j] == 1:
            G.add_edge(str(i), str(j))

# draw
nx.draw_networkx(G, node_color="k", edge_color="k", font_color="w")
plt.show()