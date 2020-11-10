#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load files
uselog = pd.read_csv('../chapter3/use_log.csv')
# print(uselog.isnull().sum())
customer = pd.read_csv('../customer_join.csv')
# print(customer.isnull().sum())

# extract data that we need to analyse
customer_clustering = customer[["mean", "median", "max", "min", "membership_period"]]
print(customer_clustering.head())
sc = StandardScaler()# setup imported library
customer_clustering_sc = sc.fit_transform(customer_clustering) # standerize data
kmeans = KMeans(n_clusters=4, random_state=0) # define a model for clustering
clusters = kmeans.fit(customer_clustering_sc) # set the data to be processed and execute clustering
customer_clustering["cluster"] = clusters.labels_ # merge results to original data
print(customer_clustering["cluster"].unique())
print(customer_clustering.head())
