#!/usr/bin/env python
# -*- coding: utf-8 -*-
# code for python3

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# set the MAX num of rows and columns that will be displayed at terminal
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)

# load files
uselog = pd.read_csv('../chapter3/use_log.csv')
# print(uselog.isnull().sum())
customer = pd.read_csv('../chapter3/customer_join.csv')
# print(customer.isnull().sum())

# extract data that we need to analyse
customer_clustering = customer[["mean", "median", "max", "min", "membership_period"]]
# print(customer_clustering.head())
sc = StandardScaler()# setup imported library
customer_clustering_sc = sc.fit_transform(customer_clustering) # standerize data
kmeans = KMeans(n_clusters=4, random_state=0) # define a model for clustering
clusters = kmeans.fit(customer_clustering_sc) # set the data to be processed and execute clustering
customer_clustering["cluster"] = clusters.labels_ # merge results to original data
# print(customer_clustering["cluster"].unique())
# print(customer_clustering.head())

# rename labels of the data
customer_clustering.columns = ["月内平均値", "月内中央値", "月内最大値", "月内最小値", "会員期間", "cluster"]
# check the num of each data
customer_clustering.groupby("cluster").count()
# print(customer_clustering.groupby("cluster").count())
# get mean value of each clusters
customer_clustering.groupby("cluster").mean()
# print(customer_clustering.groupby("cluster").mean())

# decrease dimension via principal component analysys
X = customer_clustering_sc # extract standerized data
pca = PCA(n_components=2) # define a model : decrease dimension to 2 by PCA
pca.fit(X) # execute PCA, 1st step
x_pca = pca.transform(X) # execute PCA, 2nd step
pca_df = pd.DataFrame(x_pca) # contain analysed data to new dataframe:pca_df
pca_df["cluster"] = customer_clustering["cluster"] # add clusterized data to new data

# # visualize
# for i in customer_clustering["cluster"].unique():
#     tmp = pca_df.loc[pca_df["cluster"]==i]
#     plt.scatter(tmp[0], tmp[1])
# plt.show()

# compare between clustered data and whether each customers are still in our membership
customer_clustering = pd.concat([customer_clustering, customer], axis = 1)
# analyse clusters by whether those customers are deleted from membership or not
customer_clustering.groupby(["cluster", "is_deleted"], as_index=False).count()[["cluster", "is_deleted", "customer_id"]]
# print(customer_clustering.groupby(["cluster", "is_deleted"], as_index=False).count()[["cluster", "is_deleted", "customer_id"]])
# analyse clusters by whether those customers are using our gym routinely
# customer_clustering.groupby(["cluster", "routine_flg"], as_index=False).count()[["cluster", "routine_flg", "customer_id"]]
print(customer_clustering.groupby(["cluster", "routine_flg"], as_index=False).count()[["cluster", "routine_flg", "customer_id"]])
# print(customer_clustering.head())

# # export data as csv
# customer_clustering.to_csv("customer_clustering.csv", index=False)
