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

# # draw
# nx.draw_networkx(G, node_color="k", edge_color="k", font_color="w")
# plt.show()


####################################
# visualize information transision #
####################################
# function to determin whether a certain information would be transited via word of mouth at a certain probability:percent
def determine_link(percent):
    rand_val = np.random.rand()
    if rand_val <= percent:
        return 1
    else:
        return 0

# function to reflect result of transistion by simulation


def simulate_percolation(num, list_active, percent_percolation):
    for i in range(num):
        if list_active[i] == 1:
            for j in range(num):
                if df_links.iloc[i][j] == 1:
                    if determine_link(percent_percolation) == 1:
                        list_active[j] = 1
    return list_active


percent_percolation = 0.1
T_NUM = 100  # 100 cycles for percolation(transision)
NUM = len(df_links.index)
list_active = np.zeros(NUM)
list_active[0] = 1
list_timeSeries = []
for t in range(T_NUM):
    list_active = simulate_percolation(NUM, list_active, percent_percolation)
    list_timeSeries.append(list_active.copy())

# visualize


def active_node_coloring(list_active):
    # print(list_timeSeries[t])
    list_color = []
    for i in range(len(list_timeSeries[t])):
        if list_timeSeries[t][i] == 1:
            list_color.append("r")
        else:
            list_color.append("k")
    # print(len(list_color))
    return list_color

# t = 0
# nx.draw_networkx(G, font_color = "w", node_color = active_node_coloring(list_timeSeries[t]))
# plt.show()

# t = 10
# nx.draw_networkx(G, font_color = "w", node_color = active_node_coloring(list_timeSeries[t]))
# plt.show()

# t = 99
# nx.draw_networkx(G, font_color = "w", node_color = active_node_coloring(list_timeSeries[t]))
# plt.show()


############################################
# visualize information transision by graph#
############################################
list_timeSeries_num = []
for i in range(len(list_timeSeries)):
    list_timeSeries_num.append(sum(list_timeSeries[i]))

# plt.plot(list_timeSeries_num)
# plt.show()

############################################
# simulate the num of member of our gym    #
############################################


def simulate_population(num, list_active, percent_percolation, percent_disappearence, df_links):
    # diffusion
    for i in range(num):
        if list_active[i] == 1:
            for j in range(num):
                if df_links.iloc[i][j] == 1:
                    if determine_link(percent_percolation) == 1:
                        list_active[j] = 1
    # dissapearence
    for i in range(num):
        if determine_link(percent_disappearence) == 1:
            list_active[i] = 0
    return list_active


percent_percolation = 0.1
# percent_disappearence = 0.05
percent_disappearence = 0.2
T_NUM = 100
NUM = len(df_links.index)
list_active = np.zeros(NUM)
list_active[0] = 1
list_timeSeries = []
for t in range(T_NUM):
    list_active = simulate_population(
        NUM, list_active, percent_percolation, percent_disappearence, df_links)
    list_timeSeries.append(list_active.copy())

# draw graph
list_timeSeries_num = []
for i in range(len(list_timeSeries)):
    list_timeSeries_num.append(sum(list_timeSeries[i]))

# plt.plot(list_timeSeries_num)
# plt.show()

###############################################
# get overview of parameters by phase diagram #
###############################################
T_NUM = 100
NUM_PhaseDiagram = 20
phaseDiagram = np.zeros((NUM_PhaseDiagram, NUM_PhaseDiagram))
for i_p in range(NUM_PhaseDiagram):
    for i_d in range(NUM_PhaseDiagram):
        percent_percolation = 0.05 * i_p
        percent_disappearence = 0.05 * i_d
        list_active = np.zeros(NUM)
        list_active[0] = 1
        for t in range(T_NUM):
            list_active = simulate_population(
                NUM, list_active, percent_percolation, percent_disappearence, df_links)
            phaseDiagram[i_p][i_d] = sum(list_active)

plt.matshow(phaseDiagram)
plt.colorbar(shrink = 0.8)
plt.xlabel('percent_disappearence')
plt.ylabel('percent_percolation')
plt.xticks(np.arange(0.0, 20.0, 5), np.arange(0.0, 1.0, 0.25))
plt.yticks(np.arange(0.0, 20.0, 5), np.arange(0.0, 1.0, 0.25))
plt.tick_params(bottom = False,
                left = False,
                right = False,
                top = False)
plt.show()