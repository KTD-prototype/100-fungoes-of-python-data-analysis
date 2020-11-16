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
from ortoolpy import model_min, model_max, addvars, addvals

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
m1.solve()  # solve minimization problem

# calculate total transportation cost
df_tr_sol = df_tc.copy()
total_cost = 0
for k, x in v1.items():
    i, j = k[0], k[1]
    df_tr_sol.iloc[i][j] = value(x)
    total_cost += df_tc.iloc[i][j] * value(x)
# print(df_tr_sol)
# print("総輸送コスト：" + str(total_cost))

###############################
# visualize optimized network #
# same method as 57_~~.py     #
###############################
# load data
df_tr = df_tr_sol.copy()
df_pos = pd.read_csv('trans_route_pos.csv')

# generate graph object
G = nx.Graph()

# set nodes
for i in range(len(df_pos.columns)):
    G.add_node(df_pos.columns[i])

# set dges and make a list of weights
num_pre = 0
edge_weights = []
size = 0.1
for i in range(len(df_pos.columns)):
    for j in range(len(df_pos.columns)):
        if not(i == j):
            G.add_edge(df_pos.columns[i], df_pos.columns[j])  # add edge
            # add weight of the edge
            if num_pre < len(G.edges):
                num_pre = len(G.edges)
                weight = 0
                if(df_pos.columns[i] in df_tr.columns) and (df_pos.columns[j] in df_tr.index):
                    if df_tr[df_pos.columns[i]][df_pos.columns[j]]:
                        weight = df_tr[df_pos.columns[i]
                                       ][df_pos.columns[j]] * size
                elif(df_pos.columns[j] in df_tr.columns) and (df_pos.columns[i] in df_tr.index):
                    if df_tr[df_pos.columns[j]][df_pos.columns[i]]:
                        weight = df_tr[df_pos.columns[j]
                                       ][df_pos.columns[i]] * size
                edge_weights.append(weight)

# set positions
pos = {}
for i in range(len(df_pos.columns)):
    node = df_pos.columns[i]
    pos[node] = (df_pos[node][0], df_pos[node][1])

# draw and visualize
nx.draw(G, pos, with_labels=True, font_size=16, node_size=1000,
        node_color='k', font_color='w', width=edge_weights)
# plt.show()


###############################
# check constraint conditions #
###############################
# load data
df_demand = pd.read_csv('demand.csv')
df_supply = pd.read_csv('supply.csv')

# function to calculate constraint conditions
# demand side


def condition_demand(df_tr, df_demand):
    flag = np.zeros(len(df_demand.columns))
    for i in range(len(df_demand.columns)):
        temp_sum = sum(df_tr[df_demand.columns[i]])
        if(temp_sum >= df_demand.iloc[0][i]):
            flag[i] = 1
    return flag

# supply side


def condition_supply(df_tr, df_supply):
    flag = np.zeros(len(df_supply.columns))
    for i in range(len(df_supply.columns)):
        temp_sum = sum(df_tr.loc[df_supply.columns[i]])
        if temp_sum <= df_supply.iloc[0][i]:
            flag[i] = 1
    return flag


print("需要条件計算結果：" + str(condition_demand(df_tr_sol, df_demand)))
print("供給条件計算結果：" + str(condition_supply(df_tr_sol, df_supply)))


###############################
# load production plans       #
###############################
# load data
df_material = pd.read_csv('product_plan_material.csv', index_col="製品")
df_profit = pd.read_csv('product_plan_profit.csv', index_col="製品")
df_stock = pd.read_csv('product_plan_stock.csv', index_col="項目")
df_plan = pd.read_csv('product_plan.csv', index_col="製品")
# print(df_material)
# print(df_profit)
# print(df_stock)
# print(df_plan)

# function to calculate profit


def product_plan(df_profit, df_plan):
    profit = 0
    for i in range(len(df_profit.index)):
        for j in range(len(df_plan.columns)):
            profit += df_profit.iloc[i][j] * df_plan.iloc[i][j]
    return profit


print("総利益：" + str(product_plan(df_profit, df_plan)))

###############################
# optimize production plans   #
###############################
# load data
df = df_material.copy()
inv = df_stock

m = model_max()  # declare model as maximization problem
v1 = {(i): LpVariable('v%d' % (i), lowBound=0) for i in range(len(df_profit))}
m += lpSum(df_profit.iloc[i] * v1[i] for i in range(len(df_profit)))
for i in range(len(df_material.columns)):
    m += lpSum(df_material.iloc[j, i] * v1[j]
               for j in range(len(df_profit))) <= df_stock.iloc[:, i]
m.solve()

df_plan_sol = df_plan.copy()
for k, x in v1.items():
    df_plan_sol.iloc[k] = value(x)
print(df_plan_sol)
print("総利益：" + str(value(m.objective)))


###############################
# validate optimized plans    #
###############################
def condition_stock(df_plan, df_material, df_stock):
    flag = np.zeros(len(df_material.columns))
    for i in range(len(df_material.columns)):
        temp_sum = 0
        for j in range(len(df_material.index)):
            temp_sum = temp_sum + df_material.iloc[j][i] * float(df_plan.iloc[j])
        if(temp_sum <= float(df_stock.iloc[0][i])):
            flag[i] = 1
        print(df_material.columns[i] + "　使用量：" + str(temp_sum) + ",　在庫：" + str(float(df_stock.iloc[0][i])))
    return flag

# print("制約条件計算結果：" + str(condition_stock(df_plan, df_material, df_stock)))
print("制約条件計算結果：" + str(condition_stock(df_plan_sol, df_material, df_stock)))