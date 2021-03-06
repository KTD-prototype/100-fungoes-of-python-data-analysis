#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
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
# generate graph object
G = nx.Graph()

# set node
G.add_node("nodeA")
G.add_node("nodeB")
G.add_node("nodeC")

# set edge
G.add_edge("nodeA", "nodeB")
G.add_edge("nodeA", "nodeC")
G.add_edge("nodeB", "nodeC")

# set position
pos = {}
pos["nodeA"] = (0, 0)
pos["nodeB"] = (1, 1)
pos["nodeC"] = (0, 1)

# add node
G.add_node("nodeD")
G.add_edge("nodeA", "nodeD")
pos["nodeD"] = (1, 0)

# draw and display
nx.draw(G, pos, with_labels=True)
plt.show()
