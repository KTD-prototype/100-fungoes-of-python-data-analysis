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
join_data = pd.merge(join_data, factories, left_on="ToFC", right_on="FCID", how="left")
# print(join_data.head())

# join warehouse data to joined data
join_data = pd.merge(join_data, warehouses, left_on="FromWH", right_on="WHID", how="left")
# reorder columns (do not list up unnecessary data so that you can omit from the data frame)
join_data = join_data[["TransactionDate", "Quantity", "Cost", "ToFC", "FCName", "FCDemand", "FromWH", "WHName", "WHSupply", "WHRegion"]]
# print(join_data.head())


# extract data based on branch location of the company
kanto = join_data.loc[join_data["WHRegion"]=="関東"]
tohoku = join_data.loc[join_data["WHRegion"]=="東北"]
print(kanto.head())
print('------------------------------------------------')
print(tohoku.head())