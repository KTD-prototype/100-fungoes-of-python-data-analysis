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

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load data
factories = pd.read_csv("tbl_factory.csv", index_col=0)  # factory data
warehouses = pd.read_csv("tbl_warehouse.csv", index_col=0)  # warehouse data
# transport cost data between factory and warehouse
cost = pd.read_csv("rel_cost.csv", index_col=0)
trans = pd.read_csv("tbl_transaction.csv", index_col=0)  # transaction data
# # visualize
# print(factories)
# print(warehouses)
# print(cost.head())
# print(trans.head())

# join data
# join cost data to transportation record
join_data = pd.merge(trans, cost, left_on=["ToFC", "FromWH"], right_on=[
                     "FCID", "WHID"], how="left")
# print(join_data.head())

# join factory data to joined data
join_data = pd.merge(join_data, factories, left_on="ToFC",
                     right_on="FCID", how="left")
# print(join_data.head())

# join warehouse data to joined data
join_data = pd.merge(join_data, warehouses,
                     left_on="FromWH", right_on="WHID", how="left")
# reorder columns (do not list up unnecessary data so that you can omit from the data frame)
join_data = join_data[["TransactionDate", "Quantity", "Cost", "ToFC",
                       "FCName", "FCDemand", "FromWH", "WHName", "WHSupply", "WHRegion"]]
# print(join_data.head())

# extract data based on branch location of the company
kanto = join_data.loc[join_data["WHRegion"] == "関東"]
tohoku = join_data.loc[join_data["WHRegion"] == "東北"]
# print(kanto.head())
# print('------------------------------------------------')
# print(tohoku.head())

# # check transportation cost and quantity
# print("関東支社の総コスト： " + str(kanto["Cost"].sum()) + "万円")
# print("東北支社の総コスト： " + str(tohoku["Cost"].sum()) + "万円")
# print('------------------------------------------------')
# print("関東支社の総部品輸送個数： " + str(kanto["Quantity"].sum()) + "個")
# print("東北支社の総部品輸送個数： " + str(tohoku["Quantity"].sum()) + "個")
# print('------------------------------------------------')

# # calculate cost per single parts
# tmp1 = (kanto["Cost"].sum()/kanto["Quantity"].sum()) * 10000
# tmp2 = (tohoku["Cost"].sum()/tohoku["Quantity"].sum()) * 10000
# print("関東支社の部品1つあたりの輸送コスト： " + str(int(tmp1)) + "円")
# print("東北支社の部品1つあたりの輸送コスト： " + str(int(tmp2)) + "円")
# print('------------------------------------------------')

# # calculate average cost of each delivery route
# cost_chk = pd.merge(cost, factories, on="FCID", how="left")
# print("関東支社の平均輸送コスト: " + str(cost_chk["Cost"].loc[cost_chk["FCRegion"]=="関東"].mean()) + "万円")
# print("東北支社の平均輸送コスト: " + str(cost_chk["Cost"].loc[cost_chk["FCRegion"]=="東北"].mean()) + "万円")

####################################
# visualize transportation network #
####################################
# load data to add weight data to edges
df_w = pd.read_csv('network_weight.csv')
df_p = pd.read_csv('network_pos.csv')

# make list for weights of edges
size = 10
edge_weights = []
for i in range(len(df_w)):
    for j in range(len(df_w.columns)):
        edge_weights.append(df_w.iloc[i][j] * size)

# # generate graph object
# G = nx.Graph()
# # set nodes
# for i in range(len(df_w.columns)):
#     G.add_node(df_w.columns[i])
# # set edges
# for i in range(len(df_w.columns)):
#     for j in range(len(df_w.columns)):
#         G.add_edge(df_w.columns[i], df_w.columns[j])
# # set position
# pos = {}
# for i in range(len(df_w.columns)):
#     node = df_w.columns[i]
#     pos[node] = (df_p[node][0], df_p[node][1])

# # draw and display
# nx.draw(G, pos, with_labels=True, font_size=16, node_size=1000,
#         node_color='k', font_color='w', width=edge_weights)
# plt.show()


####################################
# analyse transportation route     #
####################################
# load data
df_tr = pd.read_csv('trans_route.csv', index_col='工場')
df_pos = pd.read_csv('trans_route_pos.csv')
# print(df_tr.head())
# print(df_pos.head())

# generate graph object
G = nx.Graph()

# set nodes
for i in range(len(df_pos.columns)):
    G.add_node(df_pos.columns[i])

# set edges
num_pre = 0
edge_weights = []
size = 0.1
for i in range(len(df_pos.columns)):
    for j in range(len(df_pos.columns)):
        if not(i == j):
            # add edge
            G.add_edge(df_pos.columns[i], df_pos.columns[j])
            # add weight of the edge
            if num_pre < len(G.edges):
                num_pre = len(G.edges)
                weight = 0
                if(df_pos.columns[i] in df_tr.columns) and (df_pos.columns[j] in df_tr.index):
                    if df_tr[df_pos.columns[i]][df_pos.columns[j]]:
                        weight = df_tr[df_pos.columns[i]
                                       ][df_pos.columns[j]]*size
                elif(df_pos.columns[j] in df_tr.columns) and (df_pos.columns[i] in df_tr.index):
                    if df_tr[df_pos.columns[j]][df_pos.columns[i]]:
                        weight = df_tr[df_pos.columns[j]
                                       ][df_pos.columns[i]]*size
                edge_weights.append(weight)

# set location
pos = {}
for i in range(len(df_pos.columns)):
    node = df_pos.columns[i]
    pos[node] = (df_pos[node][0], df_pos[node][1])

# # draw and visualize
# nx.draw(G, pos, with_labels=True, font_size=16, node_size = 1000, node_color='k', font_color='w', width=edge_weights)
# plt.show()

####################################
# calculate transport cost function#
####################################
# load data
df_tr = pd.read_csv('trans_route.csv', index_col="工場")
df_tc = pd.read_csv('trans_cost.csv', index_col="工場")


# transport cost function
def trans_cost(df_tr, df_tc):
    cost = 0
    for i in range(len(df_tc.index)):
        for j in range(len(df_tr.columns)):
            cost += df_tr.iloc[i][j]*df_tc.iloc[i][j]
    return cost

print("総輸送コスト: " + str(trans_cost(df_tr, df_tc)))


####################################
# set constraint condition         #
####################################
# import data
df_tr = pd.read_csv('trans_route.csv', index_col="工場")
df_demand = pd.read_csv('demand.csv')
df_supply = pd.read_csv('supply.csv')

# constraint condition of demand side
for i in range(len(df_demand.columns)):
    temp_sum = sum(df_tr[df_demand.columns[i]])
    print(str(df_demand.columns[i]) + "への輸送量： " + str(temp_sum) + "（需要量： " + str(df_demand.iloc[0][i]) + "）")
    if temp_sum >= df_demand.iloc[0][i]:
        print("需要量を満たしています。")
    else:
        print("需要量を満たしていません。輸送ルートを再計算してください。")

# constraint condition of supply side
for i in range(len(df_supply.columns)):
    temp_sum = sum(df_tr.loc[df_supply.columns[i]])
    print(str(df_supply.columns[i]) + "からの輸送量： " + str(temp_sum) + "（供給限界： " + str(df_supply.iloc[0][i]) + "）")
    if temp_sum <= df_supply.iloc[0][i]:
        print("供給限界の範囲内です。")
    else:
        print("供給限界を超過しています。輸送ルートを再計算してください。")

